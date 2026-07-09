# limites_posicoes

Snapshots oficiais e contratos de DOM da tela `Limites de Posições`.

Status atual:
- baseline oficial registrado em `DOM-LIMITES_POSICOES-20260701-001`
- contrato resumido disponivel em `contracts/dom_contract.json`
- proposta da camada DOM disponivel em `dom_validation_proposal.md`
- checklist operacional disponivel em `validation_plan.yaml`

Quando houver mudanca relevante de DOM, registrar um novo snapshot com:

```powershell
python -m blc_adg_robot_ai.dom_registry `
  --knowledge-root "C:\Users\p-ecandido\robot_adg_project\blc-adg-robot-ai\knowledge" `
  --module "limites_posicoes" `
  --html-file "C:\temp\limites_posicoes_novo.html" `
  --story-id "EDUQ-1985" `
  --source-label "manual-browser-capture"
```

Depois do registro:

1. comparar o diff gerado em `diffs/`
2. revisar `contracts/dom_contract.json`
3. atualizar `locators/locators_map.json` e a camada Robot somente se houver impacto real
