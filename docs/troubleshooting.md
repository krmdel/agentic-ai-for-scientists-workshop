# Troubleshooting

## Dashboard shows "0 papers / 0 hypotheses" for Agentic Ai Workshop

Most common cause: symlinks didn't get created. Re-run `setup.sh`:

```bash
cd ~/Projects/agentic-ai-for-scientists-workshop
./setup.sh
```

If symlinks exist but dashboard still shows empty:

```bash
ls -la ~/Projects/organon/projects/briefs/agentic-ai-workshop/
# Every entry should be a symlink (l prefix). If you see real folders, your earlier copy is shadowing.
```

If the symlink path is wrong (`agentic-ai-workshop` repo moved or renamed):

```bash
# Re-run setup with the new path.
./setup.sh
```

## "Cannot find module 'next'" when starting the dashboard

You haven't run `npm install` in the dashboard folder:

```bash
cd ~/Projects/organon/projects/briefs/organon-dashboard
npm install
```

## Organon's `/doctor` shows "Missing environment variables" for paper-search

The `.env` shim hasn't picked up your variables. Common fixes:

```bash
# 1. Make sure .env exists at the Organon repo root:
ls ~/Projects/organon/.env

# 2. Make sure `scripts/with-env.sh` is executable:
chmod +x ~/Projects/organon/scripts/with-env.sh

# 3. Restart Claude Code (the MCP shim only reads .env at server start)
```

## Figure regeneration fails: "ModuleNotFoundError: No module named 'google.genai'"

The viz-nano-banana script needs `google-genai`. Install via `uv`:

```bash
cd ~/Projects/organon/.claude/skills/viz-nano-banana
uv run scripts/generate_image.py --prompt "test" --filename "/tmp/test.png" --dry-run
```

That triggers the inline-script dependency install.

## Obsidian doesn't show colour groups

Open the graph view → click the gear icon (top-right of the graph panel) → **Groups** section. If empty:

```bash
# Verify the config file:
cat ~/Projects/agentic-ai-for-scientists-workshop/week-01-foundations/obsidian-vault/.obsidian/graph.json | grep colorGroups
```

If `.obsidian/graph.json` is missing, run `_build_vault.py` again:

```bash
python3 ~/Projects/agentic-ai-for-scientists-workshop/week-01-foundations/scripts/_build_vault.py
```

## Symlinks broken after renaming or moving the workshop repo

Re-run `setup.sh` after the rename:

```bash
cd <new-path-to-workshop-repo>
./setup.sh
```

The script removes old symlinks (or backs up shadowing files) and creates fresh ones.

## "Permission denied" on `setup.sh`

```bash
chmod +x setup.sh
./setup.sh
```

## API rate limiting from paper-search (PubMed)

If you hit rate limits:

```bash
# In Organon's .env, set NCBI_API_KEY (free, increases rate limit from 3/s to 10/s).
# Get one at: https://www.ncbi.nlm.nih.gov/account/settings/
```

## Dashboard port 8769 already in use

```bash
lsof -ti :8769
# Kill the process or pick a different port:
cd ~/Projects/organon/projects/briefs/organon-dashboard
PORT=8770 npm run dev
```

## Still stuck

- Workshop deck → `week-01-foundations/slides/agentic-ai-workshop-week1.pdf`.
- Organon issues → see https://github.com/krmdel/organon and the README there.
- Claude Code issues → https://code.claude.com/docs/en/overview (run `/help` inside Claude Code).
