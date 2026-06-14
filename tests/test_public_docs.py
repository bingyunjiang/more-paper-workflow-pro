from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class PublicDocsTest(unittest.TestCase):
    def test_readme_has_three_public_entry_prompts(self):
        readme = read_rel("README.md")
        for token in [
            "定题入口",
            "直达下载入口",
            "写作入口",
            "examples/first-run/README.md",
        ]:
            self.assertIn(token, readme)

    def test_first_run_examples_exist(self):
        for rel in [
            "examples/first-run/README.md",
            "examples/first-run/step1-topic-sample.md",
            "examples/first-run/step5-download-summary.md",
            "examples/first-run/step7-writing-sample.md",
            "examples/demo/demo-script.md",
        ]:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_marketplace_manifest_exists(self):
        self.assertTrue((ROOT / ".claude-plugin/marketplace.json").exists())

    def test_skill_mentions_public_first_examples(self):
        skill = read_rel("SKILL.md")
        self.assertIn("Public-first entry examples", skill)
        self.assertIn("README 首屏", skill)


if __name__ == "__main__":
    unittest.main()
