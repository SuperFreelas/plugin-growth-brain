---
name: auto-learning
description: Use quando, durante uma análise, você descobrir que o dado contradiz uma premissa documentada, uma query retorna resultado inesperado, um padrão novo aparece nos dados, ou uma regra de negócio emerge do contexto. Força o registro em learnings.md antes de continuar a análise.
---

# Protocolo de auto-aprendizado

Quando descobrir algo que contradiz o que está documentado ou que surpreende,
**pare a análise e registre** em `_initiatives/<cliente deste projeto>/learnings.md`
antes de continuar. Aprender enquanto opera é o que diferencia análise séria de
análise descontextualizada.

## Quando disparar

- **Dado contradiz premissa documentada:** número do banco bate diferente do que
  a discovery/dataSpec dizem.
- **Query retorna resultado inesperado:** resultado que não faz sentido com o
  modelo mental atual.
- **Padrão novo nos dados:** algo não documentado emerge da análise.
- **Regra de negócio descoberta:** contexto operacional do cliente que afeta
  como interpretar números (ex: período de promoção, mudança de pricing,
  evento sazonal).

## Formato do append

```markdown
### [Título curto da descoberta] (descoberto em YYYY-MM-DD)
- **O que:** [fato confirmado por dado]
- **Impacto:** [como muda a análise atual e as próximas]
- **Regra:** [o que fazer diferente daqui pra frente]
```

## Regra dura

Só fatos **confirmados por dados** vão pra learnings. Hipótese não vai pra
learnings — vai pro `/hypotheses` (ICE-priorizado, com plano de teste).
Learnings é verdade observada; hipótese é aposta a testar. Misturar os dois
mata o valor de ambos.

## Depois de registrar

Volte pra análise original com o aprendizado em mente. Se o aprendizado invalida
parte do que já foi feito, refaça aquela parte — vale o tempo.
