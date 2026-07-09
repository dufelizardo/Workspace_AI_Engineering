import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from aqua_qe.dom_registry import (
    DomKnowledgeRegistry,
    build_dom_summary,
    normalize_html,
)

_SAMPLE_HTML = """
<html>
  <body>
    <h1>Limites de Posições</h1>
    <button aria-label="Confirmar">Confirmar</button>
    <button>Cancelar</button>
    <table>
      <thead><tr><th>Ativo</th><th>Limite</th></tr></thead>
    </table>
  </body>
</html>
"""

_FIXED_DT = datetime(2026, 7, 8, 12, 0, 0, tzinfo=UTC)


class TestNormalizeHtml(unittest.TestCase):
    def test_collapses_whitespace(self):
        html = "<div>  hello   world  </div>"
        result = normalize_html(html)
        self.assertNotIn("  ", result)

    def test_splits_adjacent_tags(self):
        html = "<div><span>a</span></div>"
        result = normalize_html(html)
        self.assertIn("\n", result)

    def test_empty_html(self):
        self.assertEqual(normalize_html(""), "")


class TestBuildDomSummary(unittest.TestCase):
    def test_extracts_h1(self):
        summary = build_dom_summary(_SAMPLE_HTML)
        self.assertEqual(summary["heading_h1"], "Limites de Posições")

    def test_extracts_buttons(self):
        summary = build_dom_summary(_SAMPLE_HTML)
        self.assertIn("Confirmar", summary["buttons"])
        self.assertIn("Cancelar", summary["buttons"])

    def test_extracts_table_headers(self):
        summary = build_dom_summary(_SAMPLE_HTML)
        self.assertIn("Ativo", summary["table_headers"])
        self.assertIn("Limite", summary["table_headers"])

    def test_extracts_aria_labels(self):
        summary = build_dom_summary(_SAMPLE_HTML)
        self.assertIn("Confirmar", summary["aria_labels"])

    def test_no_h1(self):
        summary = build_dom_summary("<html><body><p>sem h1</p></body></html>")
        self.assertIsNone(summary["heading_h1"])


class TestDomKnowledgeRegistry(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.registry = DomKnowledgeRegistry(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_register_creates_snapshot_file(self):
        result = self.registry.register_snapshot(
            module="limites_posicoes",
            html=_SAMPLE_HTML,
            source_label="test",
            story_id="EDUQ-1",
            captured_at=_FIXED_DT,
        )
        self.assertTrue(Path(result.snapshot_path).exists())

    def test_register_creates_contract(self):
        result = self.registry.register_snapshot(
            module="home",
            html=_SAMPLE_HTML,
            source_label="test",
            captured_at=_FIXED_DT,
        )
        contract = json.loads(Path(result.contract_path).read_text(encoding="utf-8"))
        self.assertEqual(contract["module"], "home")
        self.assertIn("dom_summary", contract)

    def test_change_id_format(self):
        result = self.registry.register_snapshot(
            module="home",
            html=_SAMPLE_HTML,
            source_label="test",
            captured_at=_FIXED_DT,
        )
        self.assertTrue(result.change_id.startswith("DOM-HOME-20260708-001"))

    def test_second_snapshot_generates_diff(self):
        self.registry.register_snapshot(
            module="home",
            html=_SAMPLE_HTML,
            source_label="test",
            captured_at=_FIXED_DT,
        )
        modified_html = _SAMPLE_HTML.replace("Confirmar", "Salvar")
        result2 = self.registry.register_snapshot(
            module="home",
            html=modified_html,
            source_label="test",
            captured_at=_FIXED_DT,
        )
        self.assertIsNotNone(result2.diff_path)
        self.assertTrue(Path(result2.diff_path).exists())

    def test_identical_snapshot_no_diff(self):
        self.registry.register_snapshot(
            module="home", html=_SAMPLE_HTML, source_label="test", captured_at=_FIXED_DT
        )
        result2 = self.registry.register_snapshot(
            module="home", html=_SAMPLE_HTML, source_label="test", captured_at=_FIXED_DT
        )
        self.assertIsNone(result2.diff_path)

    def test_index_updated(self):
        self.registry.register_snapshot(
            module="home", html=_SAMPLE_HTML, source_label="test", captured_at=_FIXED_DT
        )
        index = json.loads(self.registry.index_path.read_text(encoding="utf-8"))
        self.assertIn("home", index["modules"])
        self.assertEqual(len(index["modules"]["home"]["snapshots"]), 1)

    def test_load_current_contract(self):
        self.registry.register_snapshot(
            module="home", html=_SAMPLE_HTML, source_label="test", captured_at=_FIXED_DT
        )
        contract = self.registry.load_current_contract("home")
        self.assertIsNotNone(contract)
        self.assertEqual(contract["module"], "home")

    def test_load_contract_nonexistent_module(self):
        result = self.registry.load_current_contract("modulo_inexistente")
        self.assertIsNone(result)

    def test_slugify_module_name(self):
        result = self.registry.register_snapshot(
            module="Limites de Posições",
            html=_SAMPLE_HTML,
            source_label="test",
            captured_at=_FIXED_DT,
        )
        self.assertEqual(result.module, "limites_de_posicoes")

    def test_warning_when_screen_doesnt_match_module(self):
        result = self.registry.register_snapshot(
            module="consulta_isin",
            html=_SAMPLE_HTML,  # h1 é "Limites de Posições"
            source_label="test",
            captured_at=_FIXED_DT,
        )
        self.assertTrue(len(result.warnings) > 0)

    def test_history_file_created(self):
        result = self.registry.register_snapshot(
            module="home", html=_SAMPLE_HTML, source_label="test", captured_at=_FIXED_DT
        )
        self.assertTrue(Path(result.history_path).exists())
        history = Path(result.history_path).read_text(encoding="utf-8")
        self.assertIn("DOM-HOME", history)


if __name__ == "__main__":
    unittest.main()
