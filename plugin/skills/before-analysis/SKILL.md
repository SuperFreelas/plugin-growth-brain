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
