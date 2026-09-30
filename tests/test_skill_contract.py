"""Check that public routing and evidence boundaries survive packaging."""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_every_local_reference_in_root_exists(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        paths = re.findall(r"\]\((references/[^)]+)\)", source)
        self.assertGreaterEqual(len(paths), 4)
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())

    def test_trigger_matrix_covers_install_failure_and_adjacent_skills(self):
        cases = json.loads((ROOT / "evals/trigger_cases.json").read_text(encoding="utf-8"))
        positive = "\n".join(cases["should_trigger"])
        negative = "\n".join(cases["should_not_trigger"] + cases["near_neighbor"])
        self.assertIn("profile", positive)
        self.assertIn("remote.rss", positive)
        self.assertIn("Obsidian", negative)
        self.assertIn("skill", negative)


if __name__ == "__main__":
    unittest.main()
