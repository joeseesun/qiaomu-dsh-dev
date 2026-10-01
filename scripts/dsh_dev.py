#!/usr/bin/env python3
"""Portable DSH package helpers. No installs, profile edits or implicit shell execution."""
import argparse
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.parse
import urllib.request

SKILL = Path(__file__).resolve().parents[1]
MAX_BYTES = 100 * 1024 * 1024


def local_target(value):
    if not isinstance(value, str) or not value.startswith('./'):
        raise ValueError('Package path must start with ./')
    p = PurePosixPath(value[2:])
    if '..' in p.parts or '\\' in value or p.is_absolute() or not p.parts:
        raise ValueError('Unsafe package path')
    return str(p)


def audit(path):
    """Inspect without extracting or executing the archive."""
    errors, warnings, files = [], [], {}
    if Path(path).stat().st_size > MAX_BYTES:
        raise ValueError('Archive exceeds 100 MiB')
    with tarfile.open(path, 'r:gz') as archive:
        total = 0
        for count, member in enumerate(archive, 1):
            if count > 20000:
                raise ValueError('Too many archive entries')
            p = PurePosixPath(member.name)
            if p.is_absolute() or '..' in p.parts or '\\' in member.name or not p.parts or p.parts[0] != 'package':
                errors.append('Unsafe archive entry: ' + member.name)
                continue
            if member.isdir():
                continue
            if not member.isfile():
                errors.append('Links or special entries are not accepted: ' + member.name)
                continue
            total += member.size
            if total > MAX_BYTES:
                raise ValueError('Uncompressed archive exceeds 100 MiB')
            key = str(PurePosixPath(*p.parts[1:]))
            if key in files:
                errors.append('Duplicate archive path: ' + key)
            files[key] = member
        if 'package.json' not in files:
            raise ValueError('Missing package/package.json')
        if files['package.json'].size > 1024 * 1024:
            raise ValueError('Oversized package.json')
        package = json.load(archive.extractfile(files['package.json']))
        if not isinstance(package, dict):
            raise ValueError('package.json must be an object')

        def check_target(value, label):
            try:
                target = local_target(value)
                if not any(fnmatch.fnmatchcase(f, target) for f in files):
                    errors.append('Missing ' + label + ': ' + value)
            except ValueError as exc:
                errors.append(label + ': ' + str(exc))

        def walk_export(value):
            if isinstance(value, str):
                check_target(value, 'export')
            elif isinstance(value, dict):
                for item in value.values():
                    walk_export(item)
            elif isinstance(value, list):
                for item in value:
                    walk_export(item)
            elif value is not None:
                errors.append('Invalid export target')

        if not package.get('name') or not package.get('version'):
            errors.append('name/version required')
        if package.get('exports') is None and not package.get('main'):
            errors.append('Plugin needs exports or main')
        walk_export(package.get('exports'))
        for field in ('main', 'types', 'typings', 'icon'):
            value = package.get(field)
            if value:
                if field in ('main', 'types', 'typings') and not value.startswith('./'):
                    value = './' + value
                check_target(value, field)
        dsh = package.get('dsh', {})
        if not isinstance(dsh, dict):
            raise ValueError('dsh must be an object')
        bundle = dsh.get('bundle', {})
        patch = bundle.get('patch') if isinstance(bundle, dict) else None
        if not patch:
            errors.append('Missing dsh.bundle.patch: plain dependency does not activate a layer')
        else:
            patches = patch if isinstance(patch, list) else [patch]
            for item in patches:
                check_target(item, 'bundle patch')
        if dsh.get('profile'):
            errors.append('A distributable bundle must not declare dsh.profile')
        if dsh.get('client'):
            exports = package.get('exports', {})
            if not isinstance(exports, dict) or './client' not in exports:
                errors.append('dsh.client requires ./client export')
            warnings.append('Client factory, inject and external graph require target-runtime inspection')
        for field in ('license', 'repository', 'description'):
            if not package.get(field):
                warnings.append('Missing publishing metadata: ' + field)
        if package.get('private'):
            warnings.append('private:true blocks npm publication; Release tgz is still possible')
        for filename in files:
            parts = PurePosixPath(filename).parts
            if '.env' in parts or any(x.startswith('.env.') and x != '.env.example' for x in parts):
                errors.append('Environment file in package: ' + filename)
            if any(x in ('.git', 'node_modules', '.dsh') for x in parts):
                errors.append('Local installation content in package: ' + filename)
            if any(x in ('profiles', 'session-data', 'credentials.json') for x in parts):
                warnings.append('Review possible private runtime data: ' + filename)
        warnings.append('Static archive audit does not validate Loader YAML semantics, secrets in arbitrary files or live behavior')
    return {'ok': not errors, 'package': package.get('name'), 'version': package.get('version'),
            'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'file_count': len(files), 'errors': errors, 'warnings': warnings}


def doctor(repo, dsh=None):
    root = Path(repo).resolve()
    package_file = root / 'package.json'
    package = json.loads(package_file.read_text()) if package_file.is_file() else {}
    candidates = [dsh, shutil.which('dsh'),
                  '/Applications/DeepSeek Harness.app/Contents/Resources/runtime/cli/bin/dsh']
    candidates = list(dict.fromkeys(str(Path(x).resolve()) for x in candidates if x and Path(x).is_file()))
    missing = []

    def check(value):
        if isinstance(value, str):
            try:
                if not list(root.glob(local_target(value))):
                    missing.append(value)
            except ValueError:
                missing.append(value)
        elif isinstance(value, dict):
            for child in value.values():
                check(child)
        elif isinstance(value, list):
            for child in value:
                check(child)
    check(package.get('exports'))
    git_state = 'unavailable'
    if shutil.which('git'):
        r = subprocess.run(['git', '-C', str(root), 'status', '--short'], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            git_state = r.stdout.strip() or 'clean'
    return {'repo': str(root), 'package': package.get('name'), 'version': package.get('version'),
            'scripts': sorted(package.get('scripts', {})), 'dsh_manifest': package.get('dsh'),
            'missing_export_files': missing, 'git_status': git_state, 'cli_candidates': candidates,
            'next': 'Use the chosen target CLI --version/--help; inspect installed APIs and explicit test profile',
            'limitation': 'No CLI executed; no profile, credentials, process state or runtime verification read'}


def init_plugin(destination, name):
    if not re.fullmatch(r'(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*', name):
        raise ValueError('Use a valid lowercase npm package name')
    root = Path(destination).resolve()
    if root.exists():
        raise ValueError('Destination already exists; refusing overwrite')
    root.mkdir(parents=True)
    row = name.replace('@', '').replace('/', '-')
    package = {'name': name, 'version': '0.1.0', 'type': 'module',
               'description': 'Replace with the plugin user outcome',
               'exports': {'.': './index.js', './package.json': './package.json', './locale/*.json': './locale/*.json'},
               'icon': './icon.svg', 'files': ['index.js', 'cordis.patch.yml', 'locale', 'icon.svg'],
               'dsh': {'bundle': {'patch': './cordis.patch.yml'}}}
    (root / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
    (root / 'index.js').write_text("// Host-only bundle starting point. Add the verified business operation here.\nexport const name = " + json.dumps(row) + ";\nexport function apply(ctx) {}\n")
    (root / 'cordis.patch.yml').write_text('- insert:\n    - id: ' + row + '\n      name: ' + json.dumps(name) + '\n')
    (root / 'locale').mkdir()
    for lang in ('en', 'zh'):
        (root / 'locale' / (lang + '.json')).write_text(json.dumps({'meta': {'title': name, 'description': 'Replace with localized description'}}, indent=2) + '\n')
    (root / 'icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-16-2 20" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>\n')
    shutil.copy2(SKILL / 'templates/PLUGIN_README.md', root / 'README.md')
    shutil.copy2(SKILL / 'templates/ACCEPTANCE.md', root / 'ACCEPTANCE.md')
    (root / '.gitignore').write_text('node_modules/\n*.tgz\n.env\n.env.*\n!.env.example\n')
    return {'ok': True, 'directory': str(root), 'package': name,
            'next': 'Implement business behavior; choose source license; fill README; npm pack; audit; clean-profile activation',
            'limitation': 'Host-only empty apply, not a completed plugin or runtime-verified API scaffold'}


def verify_download(url, expected, output=None):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Use a public HTTPS URL without credentials')
    if not re.fullmatch('[a-fA-F0-9]{64}', expected):
        raise ValueError('Expected SHA256 must contain 64 hexadecimal characters')
    if output and Path(output).exists():
        raise ValueError('Output exists; refusing overwrite')
    with tempfile.TemporaryDirectory(prefix='dsh-public-') as tmp:
        path = Path(tmp) / 'package.tgz'
        req = urllib.request.Request(url, headers={'User-Agent': 'qiaomu-dsh-dev/0.2.0'})
        with urllib.request.urlopen(req, timeout=30) as response, path.open('wb') as stream:
            if urllib.parse.urlsplit(response.geturl()).scheme != 'https':
                raise ValueError('Insecure redirect')
            total = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_BYTES:
                    raise ValueError('Download exceeds 100 MiB')
                stream.write(chunk)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            raise ValueError('Public package SHA256 mismatch')
        result = audit(path)
        result['public_download_verified'] = True
        result['runtime_verified'] = False
        if output and result['ok']:
            # Exclusive creation also refuses a concurrent writer.
            with Path(output).open('xb') as target, path.open('rb') as source:
                shutil.copyfileobj(source, target)
            result['saved'] = str(Path(output).resolve())
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('doctor'); p.add_argument('--repo', required=True); p.add_argument('--dsh')
    p = commands.add_parser('init'); p.add_argument('destination'); p.add_argument('--name', required=True)
    p = commands.add_parser('audit'); p.add_argument('archive')
    p = commands.add_parser('verify-download'); p.add_argument('--url', required=True); p.add_argument('--sha256', required=True); p.add_argument('--output')
    args = parser.parse_args()
    try:
        if args.command == 'doctor':
            result = doctor(args.repo, args.dsh)
        elif args.command == 'init':
            result = init_plugin(args.destination, args.name)
        elif args.command == 'audit':
            result = audit(args.archive)
        else:
            result = verify_download(args.url, args.sha256, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get('ok', True) else 1
    except (OSError, ValueError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
