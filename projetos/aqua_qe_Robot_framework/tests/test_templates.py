import unittest

from aqua_qe.templates import LKDFTemplates


class TestLKDFTemplates(unittest.TestCase):
    def setUp(self):
        self.tmpl = LKDFTemplates(module="Limites de Posições", story_id="EDUQ-1997")

    def test_slug_removes_accents(self):
        self.assertEqual(self.tmpl.module_slug, "limites_de_posicoes")

    def test_test_suite_contains_module(self):
        content = self.tmpl.test_suite()
        self.assertIn("Limites de Posições", content)
        self.assertIn("*** Test Cases ***", content)
        self.assertIn("EDUQ-1997", content)

    def test_scenarios_imports_flows(self):
        content = self.tmpl.scenarios()
        self.assertIn("limites_de_posicoes_flows.resource", content)

    def test_flows_imports_pom(self):
        content = self.tmpl.flows()
        self.assertIn("limites_de_posicoes_pom.resource", content)

    def test_pom_has_variables(self):
        content = self.tmpl.pom()
        self.assertIn("*** Variables ***", content)
        self.assertIn("LIMITES_DE_POSICOES", content)

    def test_all_files_returns_four_layers(self):
        files = self.tmpl.all_files()
        self.assertEqual(len(files), 4)
        paths = list(files.keys())
        self.assertTrue(any("test_suites" in p for p in paths))
        self.assertTrue(any("scenarios" in p for p in paths))
        self.assertTrue(any("flows" in p for p in paths))
        self.assertTrue(any("pom" in p for p in paths))

    def test_home_module(self):
        tmpl = LKDFTemplates(module="home")
        files = tmpl.all_files()
        self.assertIn("test_suites/home/home.robot", files)


if __name__ == "__main__":
    unittest.main()
