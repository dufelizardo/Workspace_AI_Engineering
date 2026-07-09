# DOM knowledge store

Esta pasta guarda DOMs versionados por modulo para apoiar:

- validacao estrutural da UI
- auditoria de mudancas de tela
- curadoria de locators mais estaveis
- rastreabilidade entre historia, snapshot e automacao Robot

## Estrutura

```text
knowledge/dom/
  README.md
  index.json
  incoming/
  modules/
    <modulo>/
      contracts/
        dom_contract.json
      locators/
        locators_map.json
      snapshots/
        DOM-<MODULO>-YYYYMMDD-XXX.html
      diffs/
        history.md
        DOM-<MODULO>-YYYYMMDD-XXX.diff
```

## Regras operacionais

1. O HTML bruto pode entrar em `incoming/` quando vier do chat, browser ou inspeção manual.
2. O snapshot oficial deve ser registrado pelo utilitario `blc_adg_robot_ai.dom_registry`.
3. Cada registro recebe um `change_id` no formato `DOM-<MODULO>-YYYYMMDD-XXX`.
4. O contrato em `contracts/dom_contract.json` resume a tela e lista warnings de inconsistencias.
5. O arquivo `locators/locators_map.json` e manual-curated: use o snapshot como prova e ajuste os seletores com revisao.

## Observacao atual

O primeiro DOM recebido para a trilha de `limites_posicoes` apresenta titulo e labels de `Ativos Aceitos em Garantia`.
Por isso ele foi armazenado sob o modulo detectado `ativos_aceitos_garantias`, mantendo a trilha de auditoria sem contaminar `limites_posicoes`.
