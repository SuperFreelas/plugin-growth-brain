---
name: before-analysis
description: Use antes de rodar qualquer análise de growth ops (cohort, retention, equação de crescimento, hipóteses, drilldowns, etc.). Força o protocolo pré-análise que evita análises descontextualizadas — princípios + learnings + visão temporal/causal antes de qualquer query.
---

# Protocolo pré-análise

Antes de rodar **qualquer** análise de growth, execute nessa ordem:

## 0. Quota check (obrigatório, primeiro de tudo)

1. Identifique o nome do command que disparou esta skill (ex: `/hypotheses`, `/cohortAnalysis`).
2. Chame a tool MCP `record_command_run("<nome do command>")`.
3. Avalie a resposta:

   - **`blocked == true`** — pare imediatamente. Mostre ao usuário:

     ```
     ❌ Trial expirado · 30/30 análises usadas

     Pra continuar usando o Growth Brain, ative Business:
     → wa.me/5511987310294?text=Oi%20Juliano%2C%20bati%20o%20teto%20do%20trial%20e%20quero%20conversar%20sobre%20Business

     ($39/mês ou $299/ano · análises ilimitadas · onboarding 2h · suporte 24h)
     ```

     **Não execute o restante da análise.**

   - **`used >= 25`** (5 ou menos restantes) — mostre ANTES da análise:

     ```
     ⚠ {used}/30 análises do trial usadas · {remaining} restantes

     Vamos conversar sobre Business antes do teto?
     wa.me/5511987310294
     ```

     Depois prossiga normal.

   - **`used >= 20`** (10 ou menos restantes) — mostre contador discreto:

     ```
     📊 {used}/30 análises usadas · {remaining} restantes
     ```

     Depois prossiga normal.

   - **Caso contrário** (used < 20, ou tier=business): prossiga sem aviso.

**Importante:** se a tool retornar erro (DB indisponível, etc), logue e prossiga
com a análise. Cliente não pode ser refém de bug do MCP. Defesa em profundidade
existe server-side.

## 1. Princípios (obrigatório)

Chame `get_principles()` no Growth Brain. Não pule — os princípios de LTV/CAC,
payback, cashflow e cadência semanal são a régua contra a qual toda análise é
calibrada. Sem isso, a análise vira número solto sem critério.

## 2. Aprendizados acumulados (obrigatório)

Leia `_initiatives/<cliente deste projeto>/learnings.md`. Contém:
- Correções de dados passadas
- Contexto causal já confirmado
- Armadilhas conhecidas (filtros, definições, edge cases da fonte)

**Se algo no learnings.md contradiz outro documento ou seu instinto, o
learnings.md prevalece.** Aprendizado é fato confirmado por dado; o resto é
hipótese ou suposição.

## 3. Contexto de discovery (obrigatório)

Leia `_initiatives/<cliente deste projeto>/discovery.md` e verifique
se ainda contém placeholders do template (procurar por `<!-- Preencher:`
ou tabelas com linhas vazias como `| Base total | | |`).

**Se discovery.md ainda está como template (algum `<!-- Preencher:` presente):**

Avise o usuário ANTES de prosseguir, em tom convidativo (não bloqueante):

    ⚠ discovery.md ainda tem N seções com placeholders do template.

    Análises quantitativas saem normais. Mas hipóteses que dependem de
    contexto humano (o que o time já tentou, quais ferramentas usam,
    quem cuida do quê) vão sair com confiança capada — vai aparecer
    "⚠ depende de discovery" nelas.

    Quer que eu te entreviste rápido sobre as seções vazias antes
    de seguir? (Ou sigo e a gente preenche depois.)

Se o usuário pedir pra seguir sem discovery: PROSSIGA NORMAL, mas em
qualquer hipótese ou recomendação que dependa de input humano que
falte, marque explicitamente `⚠ depende de discovery` no output —
não invente contexto que não existe.

Se o usuário pedir pra fazer discovery: pause a análise, abra o
`discovery.md`, percorra as seções com `<!-- Preencher:`, faça
perguntas curtas ao usuário pra cada uma, edite o arquivo com as
respostas, e SÓ ENTÃO retome a análise.

**Se discovery.md está preenchido** (sem `<!-- Preencher:`), prossiga.

## 4. Análise sempre temporal e causal

Nunca use snapshot isolado. Sempre:
- Série temporal de 6-12 meses no mínimo (idealmente cohorts ou janelas comparáveis)
- Sempre perguntando "por quê" — correlação sem causa vira erro operacional
- Comparar com período anterior pra detectar mudança vs. ruído

## 5. Só então a análise específica

Depois dos 4 passos acima, execute a skill/command específica
(`/cohortAnalysis`, `/growthEquation`, `/retentionDrilldown`, `/hypotheses`,
etc.). Os resultados vão sair muito melhor calibrados.

A forma de executar esses passos — checklist e paralelismo — está na seção 6.

## 6. Orquestração visível (checklist + paralelismo)

*(Esta seção detalha como executar o passo 5 — não é um sexto pré-requisito do protocolo.)*

Ao executar a análise específica (passo 5), **antes de rodar os passos do
template**, materialize-os como **checklist TodoWrite** e siga as regras de
paralelismo. Isso vale para qualquer command de análise.

### 6.1 Checklist

- Crie uma lista TodoWrite com **um todo por passo procedural do template**.
  - Se o template tem seção `# Passos` (ex: `retentionDrilldown`,
    `acquisitionDrilldown`), use os passos numerados dela.
  - Se não tem (templates de report como `reportAcquisition`, `reportAffiliates`,
    que só têm `# Output`), derive um todo por **seção do Output** a produzir.
- Marque cada todo `in_progress` ao começar e `completed` **só depois que ele
  produziu o artefato** (a query foi executada e o resultado analisado — zero
  linhas é um resultado válido; a validação MECE passou; a seção do output ficou
  escrita). Não marque `completed` antecipadamente.
- Os passos 0-5 deste protocolo pré-análise **não entram** no checklist — rodam
  nos bastidores. O checklist é só dos passos da análise em si.

### 6.2 Paralelismo (quando o passo tem a tag `[paralelizável: …]`)

Alguns templates anotam um passo com `[paralelizável: …]`. Só nesses passos:

1. **Pré-requisito sequencial:** só dispare o paralelismo **depois** que todos
   os passos anteriores do checklist estiverem `completed`. Subagent nunca roda
   sobre insumo parcial (ex: a segmentação do `retentionDrilldown` exige buckets
   MECE + taxas de transição + tendência já computados).
2. **Unidade = valor de uma dimensão única:** escolha **uma** dimensão de corte
   (a mais relevante ao diagnóstico) e despache **um subagent por valor** dela —
   ex: dimensão `signup_source` → um subagent para `organic`, um para `paid`, um
   para `referral`. Nunca faça produto cartesiano de múltiplas dimensões.
3. **Teto:** no máximo 3-4 subagents por análise. Se a dimensão tem mais valores,
   pegue os mais relevantes (ex: top por volume) e trate o resto agregado.
4. **Contexto do subagent:** passe ao subagent os **learnings relevantes à fatia
   dele** (não só o recorte de dado). Se um aprendizado documentado afeta aquela
   dimensão, ele entra no briefing.
5. **Subagents não chamam MCP.** O caminho de dados é 100% local
   (`_resources/scripts/pull_data.py`). Subagents só rodam query local sobre a
   fatia e devolvem o resultado. As tools `record_command_run`, `get_principles`,
   `get_skill_template` e `get_quota_status` rodam **uma única vez no agente principal** — nunca nos subagents (senão a
   quota conta a análise N vezes).
6. **Agregação no principal:** o agente principal junta os resultados das fatias,
   só então marca o passo `completed` e segue.

Passos sem a tag `[paralelizável]` rodam **sequenciais**, como sempre.
