Gera apresentação HTML interativa a partir de uma análise existente do cliente
(hypotheses, retentionDrilldown, cohortAnalysis, growthEquation, ou qualquer
.md no projeto). Estilo dark, scroll vertical, pronto pra apresentar pro time.

## Entrada

Argumento obrigatório: caminho do `.md` fonte (relativo ao projeto do cliente).
Exemplo: `/presentation _initiatives/<cliente>/hypotheses.md`.

Se o argumento estiver vazio, peça o caminho ao usuário e pare.

## Fluxo

1. **Valida o caminho.** O arquivo precisa existir e terminar em `.md`. Se não
   existir, avise: "Arquivo não encontrado em `<path>`. Confere o caminho?"
   e pare.

2. **Leia o conteúdo do `.md` inteiro** (use a tool Read).

3. **Pergunte ao usuário a audiência:**
   > Pra quem é essa apresentação?
   > 1. Time de dados / analistas (técnico — vocabulary livre, slides densos)
   > 2. Time de operação / produto / marketing (acionável, médio nível)
   > 3. Diretoria / board / fundadores (macro, foco em $/decisão)

   Aguarde a resposta. Normalize pra `técnico`, `operacional`, ou `diretoria`
   (ex: "exec", "board", "fundador" → `diretoria`; "tecnico" sem acento →
   `técnico`; etc.). Em caso de ambiguidade, default `operacional`.

4. **Pergunte tempo de apresentação:**
   > Quanto tempo você tem?
   > 1. Lightning — 5min · 3-5 slides
   > 2. Standup — 15min · 8-12 slides
   > 3. Workshop — 30min+ · 15-20 slides

   Normalize pra `lightning`, `standup`, ou `workshop`.

5. **Chame a tool MCP** `render_presentation` com:
   - `source_path`: o caminho do .md (igual ao argumento original)
   - `source_content`: o conteúdo lido no passo 2
   - `audience`: resposta normalizada
   - `length`: resposta normalizada

6. **Trate a resposta:**
   - Se `error == "trial_quota_exceeded"`: mostre a mensagem padrão de trial
     expirado (igual a `before-analysis` skill — wa.me/5511987310294 + pricing).
     Pare aqui.
   - Se `error == "render_failed"`: mostre `"❌ Não consegui renderizar a
     apresentação. Detalhe: <detail>. Manda screenshot pro Juliano."`
     Pare aqui.
   - Se sucesso (tem `html` e `filename_hint`): siga.

7. **Garanta que existe** `_initiatives/<cliente>/presentations/`. Se não, crie
   com `mkdir -p` (use Bash).

8. **Salve o HTML retornado** em
   `_initiatives/<cliente>/presentations/<filename_hint>` (use Write).
   Se já existir um arquivo no mesmo path, sobrescreva silenciosamente
   (cliente regenerou no mesmo dia = iteração).

9. **Confirme** ao usuário com o caminho absoluto do arquivo gerado:
   > ✓ Apresentação salva em `<path>`. Abre no browser pra ver.

## Notas operacionais

- `/presentation` **não invoca** o skill `before-analysis` (não é análise nova,
  é exportação). Mas a quota é consumida via `record_command_run` server-side
  dentro do `render_presentation`.
- O HTML é estático (sem JavaScript). Pode ser compartilhado por email,
  WhatsApp, ou aberto direto no browser.
- O footer de toda slide tem link `superfreelas.com` — não desabilita
  (intencional, é attribution).
