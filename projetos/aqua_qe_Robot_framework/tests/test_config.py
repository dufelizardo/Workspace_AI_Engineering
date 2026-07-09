import unittest
from pathlib import Path

from aqua_qe.config import _DEFAULT_PROJECT, _KNOWLEDGE_BASE, AQuAConfig


class TestAQuAConfig(unittest.TestCase):
    def test_default_knowledge_root_resolves_to_default_project(self):
        config = AQuAConfig()
        self.assertEqual(config.knowledge_root, _KNOWLEDGE_BASE / _DEFAULT_PROJECT)

    def test_knowledge_root_is_path(self):
        config = AQuAConfig(knowledge_root="some/path")
        self.assertIsInstance(config.knowledge_root, Path)

    def test_from_project_sets_knowledge_root(self):
        config = AQuAConfig.from_project(project="meu_projeto")
        self.assertEqual(config.knowledge_root, _KNOWLEDGE_BASE / "meu_projeto")

    def test_from_project_knowledge_root_overrides_project(self):
        config = AQuAConfig.from_project(knowledge_root="custom/path")
        self.assertEqual(config.knowledge_root, Path("custom/path"))

    def test_from_project_accepts_path_object(self):
        config = AQuAConfig.from_project(knowledge_root=Path("meu/projeto/knowledge"))
        self.assertEqual(config.knowledge_root, Path("meu/projeto/knowledge"))

    def test_from_project_no_args_uses_default(self):
        config = AQuAConfig.from_project()
        self.assertEqual(config.knowledge_root, _KNOWLEDGE_BASE / _DEFAULT_PROJECT)


if __name__ == "__main__":
    unittest.main()
