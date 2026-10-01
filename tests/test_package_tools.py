"""Consumer artifact failures and safe helper boundaries."""
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('dsh_dev', Path(__file__).resolve().parents[1] / 'scripts/dsh_dev.py')
dev = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dev)


class PackageToolsTests(unittest.TestCase):
    def archive(self, directory, package, extra=None):
        path = Path(directory) / 'fixture.tgz'
        files = {'package.json': json.dumps(package), 'index.js': 'export function apply() {}', 'cordis.patch.yml': '- insert: []'}
        files.update(extra or {})
        with tarfile.open(path, 'w:gz') as archive:
            for name, value in files.items():
                data = value.encode(); info = tarfile.TarInfo('package/' + name); info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        return path

    def package(self):
        return {'name': 'demo-dsh', 'version': '0.1.0', 'exports': {'.': './index.js'}, 'dsh': {'bundle': {'patch': './cordis.patch.yml'}}}

    def test_scaffold_packs_without_external_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'new'; dev.init_plugin(root, 'qiaomu-demo-dsh')
            self.assertIn('dsh', json.loads((root / 'package.json').read_text()))
            with self.assertRaises(ValueError): dev.init_plugin(root, 'qiaomu-demo-dsh')

    def test_missing_types_fails_consumer_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = self.package(); package['exports']['.'] = {'default': './index.js', 'types': './types/index.d.ts'}
            result = dev.audit(self.archive(tmp, package))
            self.assertFalse(result['ok']); self.assertTrue(any('types/index.d.ts' in x for x in result['errors']))

    def test_private_tgz_allowed_and_npm_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = self.package(); package['private'] = True
            result = dev.audit(self.archive(tmp, package))
            self.assertTrue(result['ok']); self.assertTrue(any('npm' in x for x in result['warnings']))

    def test_multiple_patches_and_wildcard_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = self.package(); package['dsh']['bundle']['patch'] = ['./cordis.patch.yml', './web.patch.yml']
            package['exports']['./locale/*.json'] = './locale/*.json'
            self.assertTrue(dev.audit(self.archive(tmp, package, {'web.patch.yml': '- insert: []', 'locale/en.json': '{}'}))['ok'])

    def test_no_bundle_no_activation(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = self.package(); package.pop('dsh')
            self.assertFalse(dev.audit(self.archive(tmp, package))['ok'])

    def test_archive_traversal_and_secret_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = dev.audit(self.archive(tmp, self.package(), {'../../escape': 'x', '.env': 'DO_NOT_PUBLISH=1'}))
            self.assertFalse(result['ok']); self.assertEqual(len(result['errors']), 2)

    def test_client_metadata_needs_real_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = self.package(); package['dsh']['client'] = {'platform': 'web'}
            self.assertFalse(dev.audit(self.archive(tmp, package))['ok'])

    def test_download_rejects_credentials_before_network(self):
        with self.assertRaises(ValueError): dev.verify_download('https://user:pass@example.com/x', 'a' * 64)

    def test_download_integrity_and_exclusive_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.archive(tmp, self.package()); data = path.read_bytes()
            digest = dev.hashlib.sha256(data).hexdigest()
            def response(*args, **kwargs):
                stream = io.BytesIO(data); stream.geturl = lambda: 'https://example.com/plugin.tgz'
                return stream
            output = Path(tmp) / 'public.tgz'
            with patch.object(dev.urllib.request, 'urlopen', response):
                with self.assertRaises(ValueError): dev.verify_download('https://example.com/plugin.tgz', '0' * 64)
                result = dev.verify_download('https://example.com/plugin.tgz', digest, output)
                self.assertTrue(result['public_download_verified']); self.assertFalse(result['runtime_verified'])
                self.assertEqual(output.read_bytes(), data)
                with self.assertRaises(ValueError): dev.verify_download('https://example.com/plugin.tgz', digest, output)

    def test_archive_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'link.tgz'
            with tarfile.open(path, 'w:gz') as archive:
                payload = json.dumps(self.package()).encode()
                info = tarfile.TarInfo('package/package.json'); info.size = len(payload); archive.addfile(info, io.BytesIO(payload))
                link = tarfile.TarInfo('package/index.js'); link.type = tarfile.SYMTYPE; link.linkname = '/private/user-data'; archive.addfile(link)
            self.assertFalse(dev.audit(path)['ok'])

    def test_unsafe_package_name_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): dev.init_plugin(Path(tmp) / 'new', '../../oops')


if __name__ == '__main__':
    unittest.main()
