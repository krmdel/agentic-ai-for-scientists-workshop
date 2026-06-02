# Claude Code + Organon setup

Step-by-step install for a fresh machine. Skip what you already have.

## 1 · Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

If `claude` isn't on your PATH after install:

- macOS / Linux: check `npm config get prefix`; add `<prefix>/bin` to your shell rc.
- Windows: use the installer from anthropic.com/claude/code (recommended for Windows).

## 2 · Clone Organon

```bash
git clone https://github.com/krmdel/organon.git ~/Projects/organon
cd ~/Projects/organon
bash scripts/install.sh
```

`install.sh` does:

- Installs Python deps via `uv` (falls back to `pip` if `uv` is missing).
- Sets `+x` on shell scripts.
- Validates `.mcp.json` and the MCP-shim script.

Test:

```bash
cd ~/Projects/organon
claude
# You should see: "[heartbeat] Loading SOUL.md, USER.md, today's memory..."
# Exit with Ctrl+D.
```

## 3 · Anthropic API key

Get one at https://console.anthropic.com/. Add to Organon's `.env`:

```bash
cd ~/Projects/organon
cp .env.example .env
$EDITOR .env
# Set: ANTHROPIC_API_KEY=sk-ant-...
```

You'll also add this to the workshop repo's own `.env` later.

## 4 · Verify MCP servers

```bash
cd ~/Projects/organon
claude
# Inside: type /doctor
```

You should see green checkmarks for `paper-search`, `paperclip`, `tooluniverse`. Yellow warnings are usually missing optional API keys (NCBI, OpenAlex) — fine for the workshop.

## 5 · Continue with the workshop

Back to [SETUP.md §4](../SETUP.md#4--clone-this-workshop-repo) and clone the workshop repo.
