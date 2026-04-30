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

# Guardrail: se setup.md não existe em _initiatives/<cliente>/, avisa o Claude
# pra rodar /setup primeiro. Defesa em profundidade — também tem check duro
# nos commands de análise (skill before-analysis).
SETUP_MARKER=""
if [ -d "_initiatives" ]; then
  # Pega o primeiro subdir de _initiatives — convencionalmente é o cliente
  CLIENT_DIR=$(find _initiatives -mindepth 1 -maxdepth 1 -type d | head -n1)
  if [ -n "$CLIENT_DIR" ] && [ ! -f "$CLIENT_DIR/setup.md" ]; then
    SETUP_MARKER="ATENÇÃO: este projeto ainda não foi configurado. Rode /setup antes de qualquer comando de análise."
  fi
fi

# additionalContext do SessionStart hook é injetado no contexto da sessão.
# Formato: stdout do hook vai pro contexto se Claude Code suportar
# (depende da versão; em versões antigas pode só logar). Funciona como
# defesa em profundidade — não substitui o check explícito no /setup.
if [ -n "$SETUP_MARKER" ]; then
  echo "$SETUP_MARKER"
fi
