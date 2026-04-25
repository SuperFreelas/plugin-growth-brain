Setup inicial do projeto — rodar UMA ÚNICA VEZ, antes de qualquer comando de análise.

Siga estes passos NA ORDEM:

**1. Verifique se já rodou.** Se `_initiatives/<cliente deste projeto>/setup.md` existir, avise ao usuário que o setup já foi feito (mostre a data do arquivo) e pare. Não re-execute.

**2. Pergunte ao usuário o tipo de fonte de dados.** Opções:
   - (a) BigQuery
   - (b) Postgres / MySQL / Snowflake / outro warehouse SQL
   - (c) CSVs locais (usuário vai colocar os arquivos em `_resources/data/`)
   - (d) Outro — peça detalhes

**3. Se CSVs:** crie a pasta `_resources/data/` e instrua o usuário a colocar os arquivos lá. Os arquivos esperados seguem `_initiatives/<cliente deste projeto>/dataSpec.md` (idealmente `usuarios.csv`, `transacoes.csv`, `eventos.csv`, `custos.csv`).

**4. Abra `_initiatives/<cliente deste projeto>/dataSpec.md` e confirme com o usuário** se os campos, períodos e nomes de tabela batem com o que o cliente tem. Se não baterem, ajude o usuário a editar o dataSpec pra refletir a realidade (renomeando colunas, adicionando colunas extras, removendo que não existem).

**5. Substitua "BigQuery" pela fonte real.** Se a resposta do passo 2 NÃO foi BigQuery:
   - Use Grep ou ferramenta similar pra achar todas as ocorrências de "BigQuery" em `.claude/commands/*.md`
   - Substitua por um termo apropriado: "Postgres", "Snowflake", "CSVs locais", etc.

**6. Atualize `_resources/scripts/pull_data.py`** pro tipo de fonte escolhida:
   - BigQuery: mantém como está, só preenche `YOUR_PROJECT` e `your_dataset`
   - Postgres/outros SQL: substitui import por `psycopg2`/`sqlalchemy` e conexão apropriada
   - CSVs: substitui por `pandas.read_csv` apontando pra `_resources/data/*.csv`

**7. Escreva o marker `_initiatives/<cliente deste projeto>/setup.md`** com:
   ```markdown
   # Setup completo

   - Data: [YYYY-MM-DD]
   - Fonte de dados: [BigQuery / Postgres / CSVs / etc.]
   - Observações: [qualquer detalhe relevante do passo 4]
   ```

**8. Comunique ao usuário que o setup está completo** e ele pode rodar comandos como `/growthEquation`, `/cohortAnalysis`, `/reportRetention`.
