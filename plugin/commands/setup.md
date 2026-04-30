Setup adaptativo do projeto — rodar UMA ÚNICA VEZ, antes de qualquer comando de análise.

Identifique o `<cliente deste projeto>` lendo `_initiatives/<id>/` (apenas 1 subpasta existe).

## Verificação inicial

Se `_initiatives/<cliente>/setup.md` já existe:
- Mostre a data do arquivo.
- Avise: "Setup já foi feito em [data]. Pra refazer, use `/setup --rerun` (faz backup antes)."
- **Não execute as fases.** Pare aqui.

## Fase 0 — Onboarding (6 perguntas obrigatórias)

**Objetivo:** capturar modelo de negócio do cliente pra gerar dataSpec.md adaptado.

1. Chame a tool MCP `get_onboarding_skeleton()`. Retorna `{version, questions[]}`.
2. Para cada pergunta no array `questions`, faça **uma pergunta de cada vez** ao usuário:
   - `single_choice`: liste opções numeradas, peça pra escolher 1.
   - `multi_choice`: liste opções numeradas, peça pra escolher 1+ (separar por vírgula).
   - `free_text`: peça texto livre. Se for `id=margin` e usuário disser "não sei" / "não tenho ideia" / similar, registre como `"TBD"` (sem pedir de novo).
   - `composite`: itere as `sub` perguntas, uma de cada vez.
3. Acumule respostas num dict `answers` com as chaves correspondentes aos `id` das perguntas.
4. Quando `category == "outro"` (P1), faça **até 4 perguntas extras** adaptativas pra entender o modelo (ex: "É marketplace? B2B project-based? Ads platform?"). Anexe respostas em `answers["extras"]` (lista). Limite duro de 4 — depois prossiga.
5. Escreva `_initiatives/<cliente>/businessProfile.md` com YAML frontmatter:
   ```yaml
   ---
   skeleton_version: v1
   answered_at: <ISO timestamp UTC>
   category: <P1>
   revenue_model: <P2>
   margin: <P3>
   acquisition_channels: [<P4>]
   active_definition: <P5>
   lifecycle_milestones:
     virou_cliente_quando: <P6.1>
     ativou_quando: <P6.2>
     churnou_quando: <P6.3>
   extras: [...]  # se categoria=outro
   ---
   ```
   Body: descrição em prosa pro humano resgatar contexto depois.

## Fase 1 — Geração do dataSpec

**Objetivo:** sobrescrever o placeholder de `dataSpec.md` por um documento adaptado.

1. Chame `generate_dataspec(category=answers["category"], answers=answers)`. Retorna markdown completo.
2. Sobrescreva `_initiatives/<cliente>/dataSpec.md` com o markdown retornado.
3. Mostre o dataSpec gerado pro usuário (formate em block code ou link). Pergunte:
   - "Os campos e canônicos batem com sua realidade? Quer ajustar algo agora?"
   - Se sim, edite o arquivo conforme orientação. Se categoria=outro, **enfatize** que precisa revisar com Juliano antes de produção.
4. Sem voltar pro Fase 0 — se as respostas estavam erradas, o usuário pode rodar `/setup --rerun` depois (não nesta sessão).

## Fase 2 — Fonte de dados

**Objetivo:** conectar BigQuery / Postgres / CSV / outro.

1. Pergunte tipo de fonte:
   - (a) BigQuery
   - (b) Postgres / MySQL / Snowflake / outro warehouse SQL
   - (c) CSVs locais (`_resources/data/`)
   - (d) Outro
2. Se CSV: crie `_resources/data/`, instrua o usuário a colocar arquivos ali (`usuarios.csv`, `transacoes.csv`, `eventos.csv`, `custos.csv` ou os ajustes do dataSpec).
3. Atualize `_resources/scripts/pull_data.py` pra fonte escolhida:
   - BigQuery: preencha `YOUR_PROJECT` e `your_dataset`.
   - Postgres/SQL: troque imports por `psycopg2`/`sqlalchemy`.
   - CSV: troque por `pandas.read_csv` apontando pra `_resources/data/*.csv`.
4. Use Grep pra trocar referências hardcoded a "BigQuery" por nome real (se aplicável).

## Fase 3 — Marker de conclusão

Escreva `_initiatives/<cliente>/setup.md`:

```markdown
# Setup completo

- Data: <YYYY-MM-DD>
- Skeleton version: v1
- Categoria: <P1>
- Receita: <P2>
- Fonte de dados: <BigQuery|Postgres|CSV|...>
- Observações: <qualquer detalhe relevante das fases 1 e 2>
```

Avise o usuário: "Setup completo. Você pode rodar `/hypotheses`, `/cohortAnalysis`, `/growthEquation`, etc."

## Modo `--rerun`

Se o usuário invocar `/setup --rerun`:
1. Avise que `dataSpec.md` será regenerado e edits manuais perdidos.
2. Faça backup: `mv _initiatives/<cliente>/businessProfile.md _initiatives/<cliente>/businessProfile.md.bak-<timestamp>`.
3. Avise que `setup.md` antigo também será sobrescrito.
4. Execute Fases 0, 1, 2, 3 normalmente.
