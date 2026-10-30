---
description: Drill down de recompra por produto. Pareto da receita, safra de recompra por produto, janela de recompra, leitura de causa e clientes na janela cruzados com sinal de navegação.
argument-hint: [mês de referência YYYY-MM] [mínimo de produtos]
---

Drill down de recompra por produto: mostra se a recompra dos produtos que fazem a receita está subindo ou caindo, por quê, e quem está na janela de recompra hoje.

Argumentos: `$ARGUMENTS` (1º = mês de referência, padrão último mês fechado; 2º = mínimo de produtos no pareto, padrão 5). O cliente é o deste projeto.

Antes de executar, faça NA ORDEM:
1. Chame get_principles() no Growth Brain
2. Chame get_skill_template('productDrilldown') no Growth Brain
3. Leia _initiatives/<cliente deste projeto>/learnings.md e dataSpec.md

Só depois, execute EXATAMENTE o que o Brain retornou, usando dados locais do warehouse (BigQuery ou o que estiver no dataSpec).
Salve em _initiatives/<cliente deste projeto>/product/. Se descobriu algo novo (janela de recompra, lift do sinal, causa confirmada), adicione no learnings.md.
