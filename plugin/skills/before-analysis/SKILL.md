---
name: before-analysis
description: Use antes de rodar qualquer análise de growth ops (cohort, retention, equação de crescimento, hipóteses, drilldowns, etc.). Força o protocolo pré-análise que evita análises descontextualizadas — princípios + learnings + visão temporal/causal antes de qualquer query.
---

# Protocolo pré-análise

Antes de rodar **qualquer** análise de growth, execute nessa ordem:

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

## 3. Análise sempre temporal e causal

Nunca use snapshot isolado. Sempre:
- Série temporal de 6-12 meses no mínimo (idealmente cohorts ou janelas comparáveis)
- Sempre perguntando "por quê" — correlação sem causa vira erro operacional
- Comparar com período anterior pra detectar mudança vs. ruído

## 4. Só então a análise específica

Depois dos 3 passos acima, execute a skill/command específica
(`/cohortAnalysis`, `/growthEquation`, `/retentionDrilldown`, `/hypotheses`,
etc.). Os resultados vão sair muito melhor calibrados.
