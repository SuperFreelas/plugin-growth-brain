#!/usr/bin/env bash
# superfreelas plugin — SessionStart hook.
#
# Lê o JWT de ./.growth-brain-token (no cwd do projeto) e exporta GROWTH_BRAIN_TOKEN
# via $CLAUDE_ENV_FILE — assim a var fica disponível pro .mcp.json do plugin
# usar no header Authorization quando o MCP server inicia.
#
# Se o arquivo de token não existir, o hook não bloqueia a sessão; a primeira
# tool call vai retornar 401 e o usuário sabe o que fazer.

set -euo pipefail

TOKEN_FILE="./.growth-brain-token"

if [ ! -f "$TOKEN_FILE" ]; then
  echo "[superfreelas] .growth-brain-token não encontrado no cwd ($(pwd))." >&2
  echo "[superfreelas] Rode o Claude Code dentro da pasta do projeto entregue." >&2
  exit 0
fi

# Trim whitespace/newlines — JWT é uma linha
TOKEN=$(tr -d '[:space:]' < "$TOKEN_FILE")

if [ -z "$TOKEN" ]; then
  echo "[superfreelas] .growth-brain-token está vazio." >&2
  exit 0
fi

# CLAUDE_ENV_FILE é setado pelo Claude Code; vars escritas aí ficam no env
# de tudo que rodar depois (incluindo MCP servers). Doc oficial:
# https://code.claude.com/docs/en/hooks.md
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "GROWTH_BRAIN_TOKEN=$TOKEN" >> "$CLAUDE_ENV_FILE"
else
  # Fallback: export direto (funciona se Claude propaga o env do hook)
  export GROWTH_BRAIN_TOKEN="$TOKEN"
fi
