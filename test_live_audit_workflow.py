"""Offline contract tests for the manually pinned public live-release audit.

No network, Render token, authentication test account or production write is used.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent
WORKFLOW = ROOT / ".github/workflows/public-live-audit.yml"


class PinnedLiveAuditContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_explicit_manual_trigger_not_a_source_push(self):
        self.assertRegex(self.text, r"(?m)^on:\s*\n\s+workflow_dispatch:")
        self.assertNotRegex(self.text, r"(?m)^  (push|pull_request|schedule):")
        self.assertIn("deployed_commit_sha:", self.text)
        self.assertIn("required: true", self.text)

    def test_input_validation_and_release_checkout_are_pinned(self):
        self.assertIn('re.fullmatch(r"[0-9a-f]{40}", value)', self.text)
        self.assertIn("DEPLOYED_SHA: ${{ inputs.deployed_commit_sha }}", self.text)
        self.assertIn("ref: ${{ inputs.deployed_commit_sha }}", self.text)
        self.assertIn('git -C deployed-source rev-parse HEAD', self.text)
        self.assertIn('if [ "$actual" != "$DEPLOYED_SHA" ]; then', self.text)

    def test_auditor_is_separate_from_deployed_snapshot(self):
        self.assertIn("path: audit-tooling", self.text)
        self.assertIn("path: deployed-source", self.text)
        self.assertIn("python3 ../audit-tooling/scripts/live_audit.py", self.text)
        self.assertIn("python3 ../audit-tooling/scripts/live_browser_audit.py", self.text)
        self.assertIn("working-directory: deployed-source", self.text)
        self.assertIn("path: deployed-source/browser-audit-screenshots/", self.text)
        self.assertTrue((ROOT / "scripts/live_audit.py").is_file())
        self.assertTrue((ROOT / "scripts/live_browser_audit.py").is_file())

    def test_read_only_and_no_credentials_persisted(self):
        self.assertIn("contents: read", self.text)
        self.assertEqual(self.text.count("persist-credentials: false"), 2)
        self.assertNotRegex(self.text.lower(), r"(trigger_deploy|api[_-]?key|secrets\.)")
        self.assertIn("cancel-in-progress: false", self.text)


if __name__ == "__main__":
    unittest.main()
