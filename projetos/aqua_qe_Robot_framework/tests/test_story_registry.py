import tempfile
import unittest
from pathlib import Path

from aqua_qe.story_registry import (
    _slugify,
    register_story_artifacts,
)


class TestSlugify(unittest.TestCase):
    def test_removes_accents(self):
        self.assertEqual(_slugify("Limites de Posições"), "limites_de_posicoes")

    def test_handles_cedilla(self):
        self.assertEqual(_slugify("Acessibilidade"), "acessibilidade")

    def test_replaces_spaces_with_underscore(self):
        self.assertEqual(_slugify("home page"), "home_page")


class TestStoryRegistration(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "stories_index.yaml").write_text(
            "version: 1\nupdated_at: 1970-01-01\nstories:\n", encoding="utf-8"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_creates_story_file(self):
        result = register_story_artifacts(
            knowledge_root=self.root,
            story_id="EDUQ-1",
            module="home",
            title="Ajuste home",
        )
        story_path = self.root / "stories" / "EDUQ-1.md"
        self.assertTrue(story_path.exists())
        self.assertIn("EDUQ-1", result.created[0])

    def test_creates_stories_index_entry(self):
        register_story_artifacts(
            knowledge_root=self.root,
            story_id="EDUQ-2",
            module="limites_posicoes",
            title="Novos limites",
        )
        index_content = (self.root / "stories_index.yaml").read_text(encoding="utf-8")
        self.assertIn("EDUQ-2", index_content)
        self.assertIn("limites_posicoes", index_content)

    def test_creates_rules_delta(self):
        register_story_artifacts(
            knowledge_root=self.root,
            story_id="EDUQ-3",
            module="home",
            title="Cards home",
        )
        delta_path = self.root / "rules_delta" / "home_rules_delta.md"
        self.assertTrue(delta_path.exists())
        self.assertIn("EDUQ-3", delta_path.read_text(encoding="utf-8"))

    def test_skips_existing_story(self):
        register_story_artifacts(
            knowledge_root=self.root, story_id="EDUQ-4", module="home", title="T1"
        )
        result2 = register_story_artifacts(
            knowledge_root=self.root, story_id="EDUQ-4", module="home", title="T1"
        )
        self.assertTrue(any("EDUQ-4" in s for s in result2.skipped))

    def test_story_not_duplicated_in_index(self):
        register_story_artifacts(
            knowledge_root=self.root, story_id="EDUQ-5", module="home", title="T"
        )
        register_story_artifacts(
            knowledge_root=self.root, story_id="EDUQ-5", module="home", title="T"
        )
        index = (self.root / "stories_index.yaml").read_text(encoding="utf-8")
        self.assertEqual(index.count("story_id: EDUQ-5"), 1)

    def test_slug_applied_to_module(self):
        register_story_artifacts(
            knowledge_root=self.root,
            story_id="EDUQ-6",
            module="Limites de Posições",
            title="Test",
        )
        delta_path = self.root / "rules_delta" / "limites_de_posicoes_rules_delta.md"
        self.assertTrue(delta_path.exists())


if __name__ == "__main__":
    unittest.main()
