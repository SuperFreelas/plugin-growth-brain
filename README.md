# Plugin Growth Brain — `superfreelas`

Plugin de Claude Code que entrega a UX de growth operations:
**11 slash commands**, **2 skills metodológicas** e a configuração do MCP server
do Growth Brain.

A metodologia (frameworks, princípios, glossário) **não vive aqui** — fica
atrás do MCP autenticado por JWT. Este repo é só a casca: commands + skills +
proxy stdio que conversa com o servidor remoto.

## Quem pode instalar

Clientes ativos do Growth Brain — cada um recebe um JWT único do Juliano dentro
do scaffold do projeto deles (`<id>-growth-ops.zip`). Sem token válido, o MCP
retorna 401.

## Instalação (cliente)

Pré-requisito: você recebeu um zip `<seu-cliente>-growth-ops.zip` e o extraiu.

```bash
cd ~/projetos/<seu-cliente>-growth-ops
claude
```

Dentro do Claude Code:

```
/plugin marketplace add github.com/SuperFreelas/plugin-growth-brain
/plugin install superfreelas@superfreelas
```

Sai (`Ctrl+D`) e reabre `claude` — o stdio proxy do plugin lê o JWT de
`.growth-brain-token` no diretório do projeto e conecta ao MCP.

## Verificar instalação

```
/mcp
```

`growth-brain` deve aparecer como `connected`.

```
Liste as tools do Growth Brain
```

Se retornar a lista (`get_principles`, `get_framework`, etc), está OK.
Se der 401 ou `Failed to connect`, o token expirou — fale com o Juliano.

## O que o plugin traz

**Slash commands:**
- `/setup` — primeira configuração da fonte de dados (BigQuery / CSV / Postgres)
- `/briefing` — briefing antes da call semanal
- `/postCallLog` — processa transcrição de call em log estruturado
- `/learning` — registra um aprendizado novo
- `/cohortAnalysis` — retenção por safra (M0–M6)
- `/retentionDrilldown` — drilldown de retenção com buckets MECE
- `/growthEquation` — atualiza a equação de crescimento
- `/hypotheses` — gera hipóteses priorizadas por ICE
- `/reportRetention` — report rápido de churn
- `/reportAcquisition` — report de aquisição por canal
- `/reportAffiliates` — report de qualidade de afiliados/canais

**Skills (auto-disparam quando relevantes):**
- `before-analysis` — força protocolo pré-análise (princípios → learnings → temporal/causal)
- `auto-learning` — registra contradições no `learnings.md` antes de continuar

## Updates

Mudanças no plugin chegam aos clientes via:

```
/plugin update superfreelas
```

## Suporte

Cliente do Growth Brain? Fala com Juliano (julianoscapin@gmail.com).

Não é cliente e quer entender como funciona?
[superfreelas.com](https://superfreelas.com).
