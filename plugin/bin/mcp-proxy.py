#!/usr/bin/env python3
"""MCP stdio<->streamable-HTTP proxy pro Growth Brain.

Lê o JWT de ./.growth-brain-token (cwd do projeto) em runtime, e proxia
mensagens JSON-RPC entre stdin/stdout (Claude Code) e o MCP server remoto
(via HTTP POST com SSE response).

Stdlib only — sem pip install no scaffold do cliente.

Usado quando o plano A (env var via SessionStart hook) não funciona porque
o Claude Code não propaga $CLAUDE_ENV_FILE pro env onde o MCP inicia.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

MCP_URL = "https://growth-brain.superfreelas.com/mcp"
TOKEN_FILE = Path.cwd() / ".growth-brain-token"
TIMEOUT_SECS = 30


def _emit(obj: dict) -> None:
    """Escreve uma mensagem JSON-RPC no stdout (1 linha)."""
    sys.stdout.write(json.dumps(obj, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _emit_error(req_id, code: int, message: str) -> None:
    _emit({"jsonrpc": "2.0", "error": {"code": code, "message": message}, "id": req_id})


def _parse_sse_messages(body: str) -> list[dict]:
    """Extrai mensagens JSON-RPC de um body SSE (linhas 'data: {...}')."""
    msgs: list[dict] = []
    for line in body.splitlines():
        if line.startswith("data:"):
            payload = line[len("data:"):].strip()
            if not payload:
                continue
            try:
                msgs.append(json.loads(payload))
            except json.JSONDecodeError:
                continue
    return msgs


class Proxy:
    def __init__(self, token: str):
        self.token = token
        self.session_id: str | None = None

    def _post(self, payload: dict) -> tuple[int, str, dict[str, str]]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        req = urllib.request.Request(MCP_URL, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECS) as resp:
                resp_body = resp.read().decode("utf-8")
                resp_headers = {k: v for k, v in resp.headers.items()}
                return resp.status, resp_body, resp_headers
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            return e.code, err_body, dict(e.headers) if e.headers else {}

    def forward(self, payload: dict) -> None:
        req_id = payload.get("id")
        is_notification = "id" not in payload

        try:
            status, body, headers = self._post(payload)
        except urllib.error.URLError as e:
            if not is_notification:
                _emit_error(req_id, -32000, f"network error: {e.reason}")
            return
        except Exception as e:
            if not is_notification:
                _emit_error(req_id, -32000, f"proxy error: {e!r}")
            return

        # Captura/atualiza session id (FastMCP retorna no initialize)
        new_sid = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")
        if new_sid:
            self.session_id = new_sid

        if status == 202:
            return  # notification accepted, sem body

        if status >= 400:
            if not is_notification:
                msg = f"server returned HTTP {status}: {body[:300]}"
                _emit_error(req_id, -32000, msg)
            return

        ctype = (headers.get("Content-Type") or headers.get("content-type") or "").lower()
        if "text/event-stream" in ctype:
            for msg in _parse_sse_messages(body):
                _emit(msg)
        elif "application/json" in ctype and body.strip():
            try:
                _emit(json.loads(body))
            except json.JSONDecodeError:
                if not is_notification:
                    _emit_error(req_id, -32700, f"server returned invalid JSON: {body[:200]}")
        # Senão: 200 sem body útil (ex: notification que o server respondeu vazio) — silencioso


def _read_token() -> str | None:
    if not TOKEN_FILE.is_file():
        sys.stderr.write(
            f"[superfreelas mcp-proxy] {TOKEN_FILE} não encontrado. "
            f"Rode dentro da pasta do projeto entregue.\n"
        )
        return None
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if not token:
        sys.stderr.write(f"[superfreelas mcp-proxy] {TOKEN_FILE} está vazio.\n")
        return None
    return token


def main() -> int:
    token = _read_token()
    if token is None:
        return 1
    proxy = Proxy(token)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as e:
            _emit_error(None, -32700, f"client sent invalid JSON: {e}")
            continue
        proxy.forward(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
