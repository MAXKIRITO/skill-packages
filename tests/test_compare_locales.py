import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/i18n-check/scripts/compare_locales.py"


class CompareLocalesTests(unittest.TestCase):
    def run_compare(self, base, targets, *options):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base_file = root / "base.json"
            base_file.write_text(base, encoding="utf-8")
            command = [sys.executable, str(SCRIPT), "--base", str(base_file)]
            for index, content in enumerate(targets):
                target = root / f"target-{index}.json"
                target.write_text(content, encoding="utf-8")
                command.extend(["--locale", str(target)])
            return subprocess.run(command + list(options), capture_output=True, text=True)

    def test_translated_values_do_not_count_as_structural_differences(self):
        run = self.run_compare('{"label":"Hello","n":1}', ['{"n":1.5,"label":"你好"}'])
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_missing_extra_type_and_limit_across_multiple_locales(self):
        run = self.run_compare('{"a":"a","b":"b","n":1}',
                               ['{"n":true,"extra":"x"}', '{"a":"甲","b":"乙","n":2}'],
                               "--limit", "1")
        self.assertEqual(run.returncode, 1, run.stderr)
        first, second = json.loads(run.stdout)["reports"]
        self.assertEqual(first["missing"], {"count": 2, "items": ["/a"]})
        self.assertEqual(first["extra"]["items"], ["/extra"])
        self.assertEqual(first["type_mismatches"]["items"],
                         [{"path": "/n", "base_type": "number", "locale_type": "boolean"}])
        self.assertTrue(all(group["count"] == 0 for key, group in second.items() if key != "locale"))

    def test_literal_keys_and_nested_paths_remain_distinct(self):
        run = self.run_compare('{"a.b":"x","a":{"b":"y"},"a/b":"z","~":"t"}', ['{}'])
        self.assertEqual(run.returncode, 1)
        paths = json.loads(run.stdout)["reports"][0]["missing"]["items"]
        self.assertEqual(paths, ["/a.b", "/a/b", "/a~1b", "/~0"])

    def test_arrays_null_and_empty_containers(self):
        run = self.run_compare('{"items":["a",null],"obj":{},"arr":[]}',
                               ['{"items":["甲","乙"],"obj":[],"arr":{}}'])
        self.assertEqual(run.returncode, 1)
        mismatches = json.loads(run.stdout)["reports"][0]["type_mismatches"]
        self.assertEqual(mismatches["count"], 3)

    def test_invalid_json_duplicate_keys_and_nonobject_roots(self):
        for content in ['{"x":1,"x":2}', '{"x":NaN}', '["a"]', '{']:
            with self.subTest(content=content):
                run = self.run_compare('{}', [content])
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, "")
                self.assertIn("error", json.loads(run.stderr))

    def test_invalid_base_and_invalid_limit(self):
        self.assertEqual(self.run_compare('null', ['{}']).returncode, 2)
        self.assertEqual(self.run_compare('{}', ['{}'], '--limit', '0').returncode, 2)


if __name__ == "__main__":
    unittest.main()
