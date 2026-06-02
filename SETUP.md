# Setup — full walkthrough

For a clean machine. Skip steps you've already done.

## 1 · System dependencies

### macOS

```bash
# Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node, Python, uv, git
brew install node@20 python@3.11 uv git gh
```

### Linux (Debian / Ubuntu)

```bash
sudo apt update && sudo apt install -y nodejs npm python3 python3-pip git
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verify

```bash
node --version       # ≥ 20
python3 --version    # ≥ 3.10
uv --version
git --version
gh --version
```

## 2 · Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

If `claude` isn't on your PATH, follow the post-install prompt or see [docs/claude-code-setup.md](docs/claude-code-setup.md).

## 3 · Clone Organon (the substrate)

Organon is the agent-first template the workshop builds on. Clone it before this repo so the workshop's `setup.sh` can symlink into it.

```bash
mkdir -p ~/Projects
git clone https://github.com/krmdel/organon.git ~/Projects/organon
cd ~/Projects/organon
bash scripts/install.sh    # installs Python deps + sets file permissions
```

Test that Organon boots:

```bash
cd ~/Projects/organon
claude
# Inside Claude Code: the heartbeat should fire and run /lets-go
# Quit with Ctrl+D when the welcome message lands.
```

## 4 · Clone this workshop repo

```bash
git clone https://github.com/krmdel/agentic-ai-for-scientists-workshop.git ~/Projects/agentic-ai-for-scientists-workshop
cd ~/Projects/agentic-ai-for-scientists-workshop
```

## 5 · Run the bootstrap script

```bash
./setup.sh
```

The script:
- Detects Organon at `~/Projects/organon` (or asks for the path).
- Creates symlinks from Organon's `projects/briefs/agentic-ai-workshop/` into this repo's `week-01-foundations/` folder. The dashboard now sees the demo project.
- Copies `.env.example` → `.env` if one doesn't exist. Fill in API keys later.
- Prints next steps.

Sample successful output:

```
✓ Found Organon at /Users/you/Projects/organon
✓ Symlinked 20 paths from workshop repo into Organon
✓ Created .env (fill in keys before running the dashboard)

Next steps:
  1. Fill in .env with at least ANTHROPIC_API_KEY and GEMINI_API_KEY.
  2. Start the dashboard:    cd ~/Projects/organon/projects/briefs/organon-dashboard && npm install && npm run dev
  3. Open Obsidian → File → Open folder as vault → ~/Projects/agentic-ai-for-scientists-workshop/week-01-foundations/obsidian-vault/
```

## 6 · Fill in `.env`

```bash
cd ~/Projects/agentic-ai-for-scientists-workshop
cp .env.example .env       # (if setup.sh didn't already)
$EDITOR .env
```

Minimum:

```env
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

Optional (Week 1 live-build only):

```env
NEXT_PUBLIC_SUPABASE_URL=https://....supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

The `.env` is gitignored. Add the same keys to Organon's `.env` too if you want skills to pick them up.

## 7 · Start the dashboard

```bash
cd ~/Projects/organon/projects/briefs/organon-dashboard
npm install     # first time only
npm run dev     # opens at http://localhost:8769
```

In the project picker (top-left), select **Agentic Ai Workshop**. You should see:

- Library → 20 papers
- Hypothesis → 1 (with 4 critique tabs)
- Data → 1 file (cohort_cbc_vitals.csv, 100 rows)
- Figures → 1 image (bone marrow stress response)
- Draft → manuscript `cbc-vitals-antibiotic-response` (6 sections)
- Runs → 10 simulated workflow entries

Full dashboard guide: [docs/dashboard-setup.md](docs/dashboard-setup.md).

## 8 · Open the Obsidian vault

1. Install Obsidian: https://obsidian.md
2. Obsidian → **File → Open folder as vault**
3. Select `~/Projects/agentic-ai-for-scientists-workshop/week-01-foundations/obsidian-vault/`
4. Press **Cmd+G** for the graph view.

You should see 8 colour-coded clusters: identity (orange), concepts (gold), paper-notes (blue), experiments (red), data-notes (teal), drafts (yellow), daily (purple), inbox (grey).

Full vault guide: [docs/obsidian-setup.md](docs/obsidian-setup.md).

## 9 · You're done

The dashboard at http://localhost:8769 and the Obsidian vault both reflect the workshop's week-01 state. Edits in either place propagate to the workshop repo (via the symlinks). Commit and push to share.

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md).
