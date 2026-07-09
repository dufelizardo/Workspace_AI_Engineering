from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class LKDFTemplates:
    module: str
    story_id: str = ""

    def _slug(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[àáâãä]", "a", text)
        text = re.sub(r"[èéêë]", "e", text)
        text = re.sub(r"[ìíîï]", "i", text)
        text = re.sub(r"[òóôõö]", "o", text)
        text = re.sub(r"[ùúûü]", "u", text)
        text = re.sub(r"[ç]", "c", text)
        text = re.sub(r"[^a-z0-9]+", "_", text)
        return text.strip("_")

    @property
    def module_slug(self) -> str:
        return self._slug(self.module)

    def test_suite(self) -> str:
        m = self.module_slug
        tag = self.story_id or m
        return f"""\
*** Settings ***
Documentation    Suite de testes para o módulo {self.module}
...              Gerada pelo AQuA-QE · LKDF Layer: Test Suite
Resource         ../../src/scenarios/{m}/{m}_scenarios.resource

*** Test Cases ***
{self.module.upper()} - Smoke Inicial
    [Tags]    {m}    smoke    {tag}
    Dado que acesso o módulo {self.module}
    Então visualizo o módulo com sucesso

{self.module.upper()} - Fluxo Principal
    [Tags]    {m}    regressao    {tag}
    Dado que acesso o módulo {self.module}
    Quando executo o fluxo principal
    Então o resultado é exibido corretamente
"""

    def scenarios(self) -> str:
        m = self.module_slug
        return f"""\
*** Settings ***
Documentation    Scenarios (BDD keywords) para o módulo {self.module}
...              LKDF Layer: Scenarios
Resource         ../../src/flows/{m}/{m}_flows.resource

*** Keywords ***
Dado que acesso o módulo {self.module}
    Abrir módulo {self.module}

Quando executo o fluxo principal
    Executar fluxo principal {self.module}

Então visualizo o módulo com sucesso
    Validar carregamento {self.module}

Então o resultado é exibido corretamente
    Validar resultado {self.module}
"""

    def flows(self) -> str:
        m = self.module_slug
        return f"""\
*** Settings ***
Documentation    Flows (business keywords) para o módulo {self.module}
...              LKDF Layer: Flows
Resource         ../../src/pom/{m}/{m}_pom.resource

*** Keywords ***
Abrir módulo {self.module}
    Navegar para {self.module}
    Aguardar carregamento {self.module}

Executar fluxo principal {self.module}
    [Documentation]    Implementar fluxo principal conforme critérios de aceite
    Log    Fluxo principal do módulo {self.module}

Validar carregamento {self.module}
    Verificar elemento visível    ${{TITULO_{m.upper()}}}

Validar resultado {self.module}
    Log    Validar resultado do módulo {self.module}
"""

    def pom(self) -> str:
        m = self.module_slug
        return f"""\
*** Settings ***
Documentation    Page Object Model para o módulo {self.module}
...              LKDF Layer: POM / Locators
Library          Browser

*** Variables ***
${{URL_{m.upper()}}}          ${{BASE_URL}}/{m}
${{TITULO_{m.upper()}}}       css=h1[data-testid="{m}-title"]

*** Keywords ***
Navegar para {self.module}
    Go To    ${{URL_{m.upper()}}}

Aguardar carregamento {self.module}
    Wait For Elements State    ${{TITULO_{m.upper()}}}    visible    timeout=10s

Verificar elemento visível
    [Arguments]    ${{locator}}
    Wait For Elements State    ${{locator}}    visible    timeout=5s
"""

    def all_files(self) -> dict[str, str]:
        m = self.module_slug
        return {
            f"test_suites/{m}/{m}.robot": self.test_suite(),
            f"src/scenarios/{m}/{m}_scenarios.resource": self.scenarios(),
            f"src/flows/{m}/{m}_flows.resource": self.flows(),
            f"src/pom/{m}/{m}_pom.resource": self.pom(),
        }
