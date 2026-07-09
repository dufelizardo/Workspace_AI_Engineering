import json
import tempfile
import unittest
from pathlib import Path

from aqua_qe.validator import validate_knowledge_consistency, validate_lkdf_chain


class TestValidateLKDFChain(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _create_lkdf_files(self, module: str) -> None:
        suite_dir = self.root / "test_suites" / module
        suite_dir.mkdir(parents=True, exist_ok=True)
        (suite_dir / f"{module}.robot").write_text(
            f"*** Settings ***\nResource    ../../src/scenarios/{module}/{module}_scenarios.resource\n",
            encoding="utf-8",
        )
        scenarios = self.root / "src" / "scenarios" / module
        scenarios.mkdir(parents=True, exist_ok=True)
        (scenarios / f"{module}_scenarios.resource").write_text(
            f"*** Settings ***\nResource    ../../flows/{module}/{module}_flows.resource\n",
            encoding="utf-8",
        )
        flows = self.root / "src" / "flows" / module
        flows.mkdir(parents=True, exist_ok=True)
        (flows / f"{module}_flows.resource").write_text(
            f"*** Settings ***\nResource    ../../pom/{module}/{module}_pom.resource\n",
            encoding="utf-8",
        )
        pom = self.root / "src" / "pom" / module
        pom.mkdir(parents=True, exist_ok=True)
        (pom / f"{module}_pom.resource").write_text(
            "*** Settings ***\nLibrary    Browser\n", encoding="utf-8"
        )

    def test_valid_chain_no_errors(self):
        self._create_lkdf_files("home")
        result = validate_lkdf_chain(self.root, "home")
        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_missing_suite_file(self):
        self._create_lkdf_files("home")
        for f in (self.root / "test_suites" / "home").glob("*.robot"):
            f.unlink()
        result = validate_lkdf_chain(self.root, "home")
        self.assertFalse(result.ok)
        self.assertTrue(
            any("robot" in e.lower() or "suite" in e.lower() for e in result.errors)
        )

    def test_missing_scenarios_file(self):
        self._create_lkdf_files("home")
        (self.root / "src" / "scenarios" / "home" / "home_scenarios.resource").unlink()
        result = validate_lkdf_chain(self.root, "home")
        self.assertFalse(result.ok)

    def test_wrong_import_in_suite(self):
        self._create_lkdf_files("home")
        suite = self.root / "test_suites" / "home" / "home.robot"
        suite.write_text(
            "*** Settings ***\nResource    wrong_path.resource\n", encoding="utf-8"
        )
        result = validate_lkdf_chain(self.root, "home")
        self.assertFalse(result.ok)

    def test_validation_result_str_ok(self):
        self._create_lkdf_files("home")
        result = validate_lkdf_chain(self.root, "home")
        self.assertIn("OK", str(result))

    def test_validation_result_str_errors(self):
        result = validate_lkdf_chain(self.root, "nonexistent")
        self.assertIn("- ", str(result))


class TestValidateKnowledgeConsistency(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._write_modules_registry()

    def tearDown(self):
        self._tmp.cleanup()

    def _write_modules_registry(self) -> None:
        (self.root / "modules_registry.yaml").write_text(
            "version: 1\nmodules:\n  - module_id: home\n  - module_id: limites_posicoes\n",
            encoding="utf-8",
        )

    def _write_stories_index(self, story_id: str, module: str) -> None:
        stories_dir = self.root / "stories"
        stories_dir.mkdir(exist_ok=True)
        story_file = stories_dir / f"{story_id}.md"
        story_file.write_text(f"# {story_id}\n\n- modulo: {module}\n", encoding="utf-8")
        index = self.root / "stories_index.yaml"
        existing = (
            index.read_text(encoding="utf-8")
            if index.exists()
            else "version: 1\nstories:\n"
        )
        entry = (
            f"  - story_id: {story_id}\n"
            f"    modulo: {module}\n"
            f"    arquivo: knowledge/stories/{story_id}.md\n"
        )
        index.write_text(existing.rstrip() + "\n\n" + entry + "\n", encoding="utf-8")

    def test_empty_stories_index_is_valid(self):
        (self.root / "stories_index.yaml").write_text(
            "version: 1\nstories:\n", encoding="utf-8"
        )
        result = validate_knowledge_consistency(self.root)
        self.assertTrue(result.ok)

    def test_valid_story_no_errors(self):
        self._write_stories_index("EDUQ-1", "home")
        result = validate_knowledge_consistency(self.root)
        self.assertTrue(result.ok, f"Erros inesperados: {result.errors}")

    def test_unknown_module_raises_error(self):
        self._write_stories_index("EDUQ-2", "modulo_inexistente")
        result = validate_knowledge_consistency(self.root)
        self.assertFalse(result.ok)
        self.assertTrue(any("modulo_inexistente" in e for e in result.errors))

    def test_missing_modules_registry(self):
        (self.root / "modules_registry.yaml").unlink()
        result = validate_knowledge_consistency(self.root)
        self.assertFalse(result.ok)

    def test_dom_module_not_in_registry(self):
        (self.root / "stories_index.yaml").write_text(
            "version: 1\nstories:\n", encoding="utf-8"
        )
        dom_dir = (
            self.root / "dom" / "modules" / "modulo_dom_desconhecido" / "contracts"
        )
        dom_dir.mkdir(parents=True)
        dom_index = self.root / "dom" / "index.json"
        dom_index.parent.mkdir(exist_ok=True)
        dom_index.write_text(
            json.dumps(
                {
                    "version": 1,
                    "modules": {"modulo_dom_desconhecido": {"snapshots": []}},
                }
            ),
            encoding="utf-8",
        )
        result = validate_knowledge_consistency(self.root)
        self.assertFalse(result.ok)
        self.assertTrue(any("modulo_dom_desconhecido" in e for e in result.errors))


if __name__ == "__main__":
    unittest.main()
