import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("template_check", ROOT / "tools/check.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class TemplateTests(unittest.TestCase):
    def test_repository(self):
        self.assertEqual(checker.check(ROOT), [])

    def test_missing_templates_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(checker.check(Path(directory)))

    def test_broken_link_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[missing](absent.md)", encoding="utf-8")
            self.assertTrue(any("broken/outside" in e for e in checker.check(root)))

    def test_symlink_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").symlink_to("absent.md")
            self.assertTrue(any("symlink" in e for e in checker.check(root)))

    def test_private_home_signal(self):
        self.assertIn("private home path", checker.signals("/" + "Users" + "/fictional/example"))

    def test_key_signal(self):
        self.assertIn("private key block", checker.signals("-----BEGIN " + "PRIVATE KEY-----"))

    def test_credential_signal(self):
        self.assertIn("access credential", checker.signals("ghp_" + "a" * 30))

    def test_public_link_allowed(self):
        self.assertEqual(checker.signals("https://github.com/meo9805/agent-home-template"), [])

    def test_examples_are_explicitly_fictional(self):
        for path in (ROOT / "examples").rglob("*.md"):
            self.assertIn("虚构", path.read_text(encoding="utf-8"), path.name)

    def test_no_private_history_or_runtime_promises(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("未提供执行器", readme)
        self.assertIn("不能替代完整隐私", readme)


if __name__ == "__main__":
    unittest.main()
