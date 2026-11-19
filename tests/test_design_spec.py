import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY_SCRIPT = ROOT / "skills/human-design-thinking/scripts/verify_design_spec.py"
GENERATE_SCRIPT = ROOT / "skills/human-design-thinking/scripts/generate_tokens.py"
TEMPLATE_SPEC = ROOT / "skills/human-design-thinking/references/DESIGN_SPEC_TEMPLATE.md"


class DesignSpecTests(unittest.TestCase):
    def test_verify_design_spec_passes_template(self):
        command = [sys.executable, str(VERIFY_SCRIPT), "--spec", str(TEMPLATE_SPEC), "--json"]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, f"Template should pass: {run.stderr}")
        data = json.loads(run.stdout)
        self.assertTrue(data["passed"])
        self.assertEqual(data["score"], 100)
        self.assertEqual(len(data["checklist"]["missing_states"]), 0)

    def test_verify_design_spec_catches_missing_states(self):
        invalid_content = """# Minimal Spec
## 1. Persona & Context
Core task: User clicks button.
Content-first: real title.

## 2. 60-30-10 Color System
Uses oklch colors.

## 3. Typography & 8pt grid
Modular type scale and 8pt spacing.

## 4. Components
Only has Default and Hover state. No other states!

## 5. Adversarial Critique
Critic challenged and Lead arbitrated trade-off.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
            f.write(invalid_content)
            temp_path = f.name

        try:
            command = [sys.executable, str(VERIFY_SCRIPT), "--spec", temp_path, "--json"]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, "Spec with missing states should exit with code 1")
            data = json.loads(run.stdout)
            self.assertFalse(data["passed"])
            # Should identify missing states: focus, active, disabled, loading, error, empty
            missing = data["checklist"]["missing_states"]
            self.assertIn("focus", missing)
            self.assertIn("disabled", missing)
            self.assertIn("loading", missing)
            self.assertIn("error", missing)
            self.assertIn("empty", missing)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_verify_design_spec_catches_missing_adversarial_log(self):
        no_debate_content = """# Spec without debate
## 1. Persona and user core task
Content-first real title.
## 2. 60-30-10 oklch color
## 3. Modular type scale & 8pt grid
## 4. States
Default Hover Focus Active Disabled Loading Error Empty
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
            f.write(no_debate_content)
            temp_path = f.name

        try:
            command = [sys.executable, str(VERIFY_SCRIPT), "--spec", temp_path, "--json"]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            data = json.loads(run.stdout)
            self.assertFalse(data["checklist"]["has_adversarial_critique"])
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_generate_tokens_valid_json_and_css(self):
        # Test JSON generation
        cmd_json = [sys.executable, str(GENERATE_SCRIPT), "--brand", "#3B82F6", "--format", "json"]
        run_json = subprocess.run(cmd_json, capture_output=True, text=True)
        self.assertEqual(run_json.returncode, 0, run_json.stderr)
        tokens = json.loads(run_json.stdout)
        self.assertIn("primitive", tokens)
        self.assertIn("semantic", tokens)
        self.assertIn("component", tokens)
        self.assertIn("space-4", tokens["primitive"]["space"])
        self.assertEqual(tokens["primitive"]["space"]["space-4"], "16px")

        # Test CSS generation
        cmd_css = [sys.executable, str(GENERATE_SCRIPT), "--brand", "#3B82F6", "--format", "css"]
        run_css = subprocess.run(cmd_css, capture_output=True, text=True)
        self.assertEqual(run_css.returncode, 0, run_css.stderr)
        css = run_css.stdout
        self.assertIn("--space-4: 16px;", css)
        self.assertIn("--color-action-primary: oklch(", css)
        self.assertIn("@media (prefers-color-scheme: dark)", css)


if __name__ == "__main__":
    unittest.main()
