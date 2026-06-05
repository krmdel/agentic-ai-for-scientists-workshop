#!/usr/bin/env bash
# Bootstrap the workshop repo on a fresh laptop.
# - Verifies prerequisites
# - Detects Organon repo location (or prompts)
# - Creates symlinks from Organon into this repo so the dashboard resolves the demo project
# - Copies .env.example → .env

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_REPO="$SCRIPT_DIR"
WEEK="week-01-foundations"

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

ok()    { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn()  { printf "${YELLOW}!${NC} %s\n" "$1"; }
fail()  { printf "${RED}✗${NC} %s\n" "$1"; }
step()  { printf "\n${BOLD}%s${NC}\n" "$1"; }

step "1. Checking prerequisites"

missing=()
command -v node    >/dev/null 2>&1 || missing+=("node (≥ 20)")
command -v python3 >/dev/null 2>&1 || missing+=("python3 (≥ 3.10)")
command -v git     >/dev/null 2>&1 || missing+=("git")
command -v claude  >/dev/null 2>&1 || missing+=("claude (npm install -g @anthropic-ai/claude-code)")

if [ ${#missing[@]} -gt 0 ]; then
  fail "Missing prerequisites:"
  for m in "${missing[@]}"; do echo "    - $m"; done
  echo ""
  echo "See SETUP.md §1 for install instructions."
  exit 1
fi
ok "node, python3, git, claude all available"

step "2. Locating Organon repo"

ORGANON_DEFAULT="$HOME/Projects/organon"
if [ -n "${ORGANON_ROOT:-}" ] && [ -d "$ORGANON_ROOT" ]; then
  ORGANON="$ORGANON_ROOT"
  ok "Using \$ORGANON_ROOT = $ORGANON"
elif [ -d "$ORGANON_DEFAULT" ]; then
  ORGANON="$ORGANON_DEFAULT"
  ok "Found Organon at $ORGANON"
else
  warn "Organon not found at $ORGANON_DEFAULT"
  read -r -p "Path to your Organon clone (or blank to clone it now): " ORGANON
  if [ -z "$ORGANON" ]; then
    echo "Cloning Organon to $ORGANON_DEFAULT..."
    git clone https://github.com/krmdel/organon.git "$ORGANON_DEFAULT"
    ORGANON="$ORGANON_DEFAULT"
    cd "$ORGANON" && bash scripts/install.sh && cd "$WORKSHOP_REPO"
  fi
  if [ ! -d "$ORGANON" ]; then
    fail "Organon path does not exist: $ORGANON"
    exit 1
  fi
fi

if [ ! -f "$ORGANON/CLAUDE.md" ]; then
  fail "$ORGANON does not look like an Organon repo (no CLAUDE.md). Aborting."
  exit 1
fi

step "3. Symlinking workshop content into Organon"

BRIEF_DIR="$ORGANON/projects/briefs/agentic-ai-workshop"
mkdir -p "$BRIEF_DIR"

# Pairs: <link-name-under-brief>  <target-path-in-workshop-repo>
link_specs=(
  "papers              $WEEK/dashboard-project/papers"
  "hypotheses          $WEEK/dashboard-project/hypotheses"
  "data                $WEEK/dashboard-project/data"
  "figures             $WEEK/dashboard-project/figures"
  "manuscripts         $WEEK/dashboard-project/manuscripts"
  ".organon            $WEEK/dashboard-project/.organon"
  "obsidian-vault      $WEEK/obsidian-vault"
  "brief.md            $WEEK/brief.md"
  "talk-notes.md       $WEEK/talk-notes.md"
  "WORKSHOP_PROMPTS.md $WEEK/WORKSHOP_PROMPTS.md"
  "assets              $WEEK/assets"
  "agentic-ai-workshop-week1.pdf   $WEEK/slides/agentic-ai-workshop-week1.pdf"
)

count=0
for spec in "${link_specs[@]}"; do
  link_name=$(echo "$spec" | awk '{print $1}')
  target_rel=$(echo "$spec" | awk '{print $2}')
  target_abs="$WORKSHOP_REPO/$target_rel"
  link_abs="$BRIEF_DIR/$link_name"

  if [ ! -e "$target_abs" ]; then
    continue   # target doesn't exist yet (e.g. slides not added) — skip silently
  fi

  if [ -L "$link_abs" ]; then
    rm "$link_abs"
  elif [ -e "$link_abs" ]; then
    # If a real file/dir is there, back it up rather than overwrite
    mv "$link_abs" "${link_abs}.backup-$(date +%s)"
    warn "Backed up existing $link_name → ${link_name}.backup-…"
  fi

  ln -s "$target_abs" "$link_abs"
  count=$((count + 1))
done

ok "Created $count symlinks in $BRIEF_DIR/"

step "4. Setting up .env"

if [ -f "$WORKSHOP_REPO/.env" ]; then
  ok ".env already exists — not overwriting"
else
  if [ -f "$WORKSHOP_REPO/.env.example" ]; then
    cp "$WORKSHOP_REPO/.env.example" "$WORKSHOP_REPO/.env"
    ok "Created .env from .env.example"
    warn "Fill in ANTHROPIC_API_KEY and GEMINI_API_KEY before running the dashboard."
  fi
fi

step "5. Done"

cat <<EOF

Next steps:

  1. Fill in .env with at least ANTHROPIC_API_KEY and GEMINI_API_KEY:
       \$EDITOR $WORKSHOP_REPO/.env

  2. Start the Organon dashboard:
       cd $ORGANON/projects/briefs/organon-dashboard
       npm install     # first time only
       npm run dev     # opens at http://localhost:8769

     In the project picker, select "Agentic Ai Workshop". You should see:
     Library (20 papers), Hypothesis (1), Data (1 cohort), Figures (1),
     Draft (6 sections), Runs (10).

  3. Open Obsidian → File → Open folder as vault →
       $WORKSHOP_REPO/$WEEK/obsidian-vault/
     Press Cmd+G for the graph view.

  Full walkthrough:  SETUP.md
  Troubleshooting:   docs/troubleshooting.md

EOF
