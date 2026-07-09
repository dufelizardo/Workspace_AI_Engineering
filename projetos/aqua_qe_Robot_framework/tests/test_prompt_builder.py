import tempfile
import unittest
from pathlib import Path

from aqua_qe.prompt_builder import AQuAPromptBuilder


def _make_knowledge(root: Path) -> None:
    """Popula uma base de conhecimento mínima para testes."""
    (root / "modules_registry.yaml").write_text(
        "version: 1\nmodules:\n  - module_id: home\n  - module_id: limites_posicoes\n",
        encoding="utf-8",
    )
    (root / "stories_index.yaml").write_text(
        "version: 1\nstories:\n"
        "  - story_id: EDUQ-90\n    modulo: home\n    arquivo: knowledge/stories/EDUQ-90.md\n",
        encoding="utf-8",
    )
    stories_dir = root / "stories"
    stories_dir.mkdir()
    (stories_dir / "EDUQ-90.md").write_text(
        "# EDUQ-90 [HOME]\n\n- modulo: home\n\n## Objetivo\nAjuste nos cards da home.\n",
        encoding="utf-8",
    )


class TestAQuAPromptBuilder(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _make_knowledge(self.root)
        self.builder = AQuAPromptBuilder(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    # ------------------------------------------------------------------
    # story_context
    # ------------------------------------------------------------------

    def test_story_context_contains_methodology(self):
        prompt = self.builder.story_context(story_text="Como usuário quero X")
        self.assertIn("LKDF", prompt)
        self.assertIn("Test Suite", prompt)

    def test_story_context_contains_pom_naming_convention(self):
        prompt = self.builder.story_context(story_text="Como usuário quero X")
        self.assertIn("Home - Navegar para Home", prompt)
        self.assertIn("pom.resource", prompt)

    def test_story_context_includes_modules_registry(self):
        prompt = self.builder.story_context(story_text="história qualquer")
        self.assertIn("modules_registry", prompt)
        self.assertIn("home", prompt)

    def test_story_context_includes_story_text(self):
        story = "Como Gestor quero ver cards na Home"
        prompt = self.builder.story_context(story_text=story)
        self.assertIn(story, prompt)

    def test_story_context_includes_story_id(self):
        prompt = self.builder.story_context(story_text="texto", story_id="EDUQ-90")
        self.assertIn("EDUQ-90", prompt)

    def test_story_context_analyze_asks_for_project(self):
        prompt = self.builder.story_context(story_text="história", task="analyze")
        self.assertIn("projeto Robot Framework", prompt)

    def test_story_context_generate_task(self):
        prompt = self.builder.story_context(story_text="história", task="generate")
        # O prompt de geração deve pedir confirmação do projeto alvo
        self.assertIn("projeto Robot Framework", prompt)

    def test_story_context_with_module_loads_stories(self):
        prompt = self.builder.story_context(story_text="nova história", module="home")
        # Deve incluir histórias existentes do módulo home para contexto
        self.assertIn("EDUQ-90", prompt)

    # ------------------------------------------------------------------
    # knowledge_context
    # ------------------------------------------------------------------

    def test_knowledge_context_includes_query(self):
        prompt = self.builder.knowledge_context(query="Quais módulos existem?")
        self.assertIn("Quais módulos existem?", prompt)

    def test_knowledge_context_scope_modules(self):
        prompt = self.builder.knowledge_context(query="módulos", scope="modules")
        self.assertIn("modules_registry", prompt)

    def test_knowledge_context_scope_stories(self):
        prompt = self.builder.knowledge_context(query="histórias", scope="stories")
        self.assertIn("stories_index", prompt)

    # ------------------------------------------------------------------
    # dom_context
    # ------------------------------------------------------------------

    def test_dom_context_includes_html(self):
        html = "<html><h1>Home</h1></html>"
        prompt = self.builder.dom_context(module="home", html_snippet=html)
        self.assertIn("Home", prompt)

    def test_dom_context_includes_module(self):
        prompt = self.builder.dom_context(module="home", html_snippet="<html/>")
        self.assertIn("home", prompt)

    def test_dom_context_with_story_id(self):
        prompt = self.builder.dom_context(
            module="home", html_snippet="<html/>", story_id="EDUQ-99"
        )
        self.assertIn("EDUQ-99", prompt)

    def test_dom_context_with_previous_contract(self):
        contract = {"module": "home", "dom_summary": {"heading_h1": "Home"}}
        prompt = self.builder.dom_context(
            module="home", html_snippet="<html/>", previous_contract=contract
        )
        self.assertIn("Contrato DOM anterior", prompt)

    def test_dom_context_asks_for_project(self):
        prompt = self.builder.dom_context(module="home", html_snippet="<html/>")
        self.assertIn("projeto Robot Framework", prompt)

    # ------------------------------------------------------------------
    # format_for_terminal
    # ------------------------------------------------------------------

    def test_format_for_terminal_has_separator(self):
        result = self.builder.format_for_terminal("conteúdo do prompt")
        self.assertIn("=" * 72, result)
        self.assertIn("conteúdo do prompt", result)

    # ------------------------------------------------------------------
    # _load_knowledge
    # ------------------------------------------------------------------

    def test_load_knowledge_empty_root_returns_empty(self):
        empty_root = self.root / "nao_existe"
        builder = AQuAPromptBuilder(empty_root)
        result = builder._load_knowledge()
        self.assertEqual(result, "")

    def test_load_knowledge_all_scope(self):
        result = self.builder._load_knowledge(scope="all")
        self.assertIn("modules_registry", result)
        self.assertIn("stories_index", result)


if __name__ == "__main__":
    unittest.main()
