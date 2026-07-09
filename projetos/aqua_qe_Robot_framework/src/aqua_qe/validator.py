"""Validação da cadeia LKDF e consistência da base de conhecimento."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    errors: list[str]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def __str__(self) -> str:
        if self.ok:
            return "OK — nenhum erro encontrado."
        return "\n".join(f"- {e}" for e in self.errors)


def validate_lkdf_chain(target_root: Path, module: str = "home") -> ValidationResult:
    """Valida a cadeia LKDF (4 camadas) de um módulo e retorna erros."""
    module = module.lower()
    errors: list[str] = []

    suite_dir = target_root / "test_suites" / module
    suite_files = sorted(suite_dir.glob("*.robot")) if suite_dir.exists() else []
    scenarios = (
        target_root / "src" / "scenarios" / module / f"{module}_scenarios.resource"
    )
    flows = target_root / "src" / "flows" / module / f"{module}_flows.resource"
    pom = target_root / "src" / "pom" / module / f"{module}_pom.resource"

    if not suite_files:
        errors.append(f"Sem arquivos .robot em: {suite_dir}")
    if not scenarios.exists():
        errors.append(f"Arquivo de scenarios não encontrado: {scenarios}")
    if not flows.exists():
        errors.append(f"Arquivo de flows não encontrado: {flows}")
    if not pom.exists():
        errors.append(f"Arquivo de POM não encontrado: {pom}")

    expected_suite_import = f"../../src/scenarios/{module}/{module}_scenarios.resource"
    if suite_files:
        has_valid = any(
            _has_resource_import(f, expected_suite_import) for f in suite_files
        )
        if not has_valid:
            errors.append(f"Import inválido ou ausente em test_suites/{module}/*.robot")

    expected_scenarios_import = f"../../flows/{module}/{module}_flows.resource"
    if scenarios.exists() and not _has_resource_import(
        scenarios, expected_scenarios_import
    ):
        errors.append(f"Import inválido ou ausente em {scenarios}")

    expected_flows_import = f"../../pom/{module}/{module}_pom.resource"
    if flows.exists() and not _has_resource_import(flows, expected_flows_import):
        errors.append(f"Import inválido ou ausente em {flows}")

    return ValidationResult(errors=errors)


def validate_knowledge_consistency(knowledge_root: Path) -> ValidationResult:
    """Valida consistência entre módulos, histórias e DOM contracts."""
    errors: list[str] = []

    modules_registry_path = knowledge_root / "modules_registry.yaml"
    stories_index_path = knowledge_root / "stories_index.yaml"

    if not modules_registry_path.exists():
        return ValidationResult(
            errors=[f"modules_registry.yaml não encontrado: {modules_registry_path}"]
        )
    if not stories_index_path.exists():
        return ValidationResult(
            errors=[f"stories_index.yaml não encontrado: {stories_index_path}"]
        )

    modules = _load_modules_registry(modules_registry_path)
    if not modules:
        return ValidationResult(
            errors=[f"Nenhum module_id encontrado em {modules_registry_path}"]
        )

    stories = _load_stories_index(stories_index_path)
    story_ids = {s["story_id"] for s in stories if s.get("story_id")}

    for story in stories:
        story_id = story.get("story_id")
        module = story.get("modulo")
        relative_file = story.get("arquivo")

        if not story_id:
            errors.append("Entrada sem story_id em stories_index.yaml")
            continue
        if not module:
            errors.append(
                f"História {story_id} sem campo 'modulo' em stories_index.yaml"
            )
            continue
        if module not in modules:
            errors.append(
                f"História {story_id} referencia módulo desconhecido '{module}' "
                f"(não registrado em modules_registry.yaml)"
            )
        if not relative_file:
            errors.append(
                f"História {story_id} sem campo 'arquivo' em stories_index.yaml"
            )
            continue

        story_path = (
            knowledge_root.parent / relative_file
            if not relative_file.startswith("/")
            else Path(relative_file)
        )
        if not story_path.exists():
            story_path = knowledge_root / "stories" / f"{story_id}.md"
        if not story_path.exists():
            errors.append(
                f"Arquivo de história não encontrado para {story_id}: {story_path}"
            )
            continue

        metadata_module = _extract_story_metadata_module(story_path)
        if not metadata_module:
            errors.append(f"Campo 'modulo' ausente nos metadados de {story_path}")
        elif metadata_module != module:
            errors.append(
                f"Módulo divergente em {story_id}: "
                f"index='{module}' vs metadata='{metadata_module}'"
            )

    dom_index_path = knowledge_root / "dom" / "index.json"
    if not dom_index_path.exists():
        return ValidationResult(errors=errors)

    dom_index = json.loads(dom_index_path.read_text(encoding="utf-8"))
    for dom_module_key, dom_module in dom_index.get("modules", {}).items():
        if dom_module_key not in modules:
            errors.append(
                f"Módulo DOM '{dom_module_key}' não registrado em modules_registry.yaml"
            )

        snapshots = dom_module.get("snapshots", [])
        if not snapshots:
            continue

        latest = snapshots[-1]
        latest_story_id = latest.get("story_id")
        if not latest_story_id:
            errors.append(
                f"Snapshot DOM mais recente sem story_id — módulo '{dom_module_key}'"
            )
        elif latest_story_id not in story_ids:
            errors.append(
                f"story_id '{latest_story_id}' do snapshot DOM de '{dom_module_key}' "
                f"não encontrado em stories_index.yaml"
            )

        contract_path = (
            knowledge_root
            / "dom"
            / "modules"
            / dom_module_key
            / "contracts"
            / "dom_contract.json"
        )
        if not contract_path.exists():
            errors.append(
                f"dom_contract.json ausente para módulo '{dom_module_key}': {contract_path}"
            )
            continue

        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        contract_story_id = contract.get("story_id")
        if not contract_story_id:
            errors.append(f"story_id vazio no dom_contract.json de '{dom_module_key}'")
        elif contract_story_id not in story_ids:
            errors.append(
                f"story_id '{contract_story_id}' do dom_contract de '{dom_module_key}' "
                f"não encontrado em stories_index.yaml"
            )

        if (
            latest_story_id
            and contract_story_id
            and latest_story_id != contract_story_id
        ):
            errors.append(
                f"Divergência em '{dom_module_key}': snapshot story='{latest_story_id}' "
                f"vs contract story='{contract_story_id}'"
            )

    return ValidationResult(errors=errors)


def _has_resource_import(file_path: Path, expected_import: str) -> bool:
    if not file_path.exists():
        return False
    content = file_path.read_text(encoding="utf-8")
    pattern = rf"^\s*Resource\s+{re.escape(expected_import)}\s*$"
    return re.search(pattern, content, flags=re.MULTILINE) is not None


def _load_modules_registry(file_path: Path) -> set[str]:
    modules: set[str] = set()
    for line in file_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*-\s*module_id:\s*([a-z0-9_]+)\s*$", line)
        if match:
            modules.add(match.group(1))
    return modules


def _load_stories_index(file_path: Path) -> list[dict[str, str]]:
    stories: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("  - story_id:"):
            if current:
                stories.append(current)
            current = {"story_id": line.split(":", 1)[1].strip()}
            continue
        if not current:
            continue
        if line.startswith("    modulo:"):
            current["modulo"] = line.split(":", 1)[1].strip()
        elif line.startswith("    arquivo:"):
            current["arquivo"] = line.split(":", 1)[1].strip()

    if current:
        stories.append(current)
    return stories


def _extract_story_metadata_module(story_path: Path) -> str | None:
    content = story_path.read_text(encoding="utf-8")
    match = re.search(r"^- modulo:\s*(.+)$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else None
