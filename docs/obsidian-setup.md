# Obsidian Vault setup

The workshop vault is a standalone Obsidian vault, pre-populated with 43 cross-linked notes. It is **separate** from any personal vault on your machine; opening it never touches your existing notes.

## 1 · Install Obsidian

Free from https://obsidian.md. No account required.

## 2 · Open the vault

1. Obsidian → **File → Open folder as vault**.
2. Navigate to:
   ```
   ~/Projects/agentic-ai-for-scientists-workshop/week-01-foundations/obsidian-vault/
   ```
3. Click **Open**.

On first open Obsidian may ask whether to trust the vault — yes, this is your own clone of the repo.

## 3 · See the graph

Cmd+G (Mac) or Ctrl+G (Linux/Windows) opens the **Graph view**. You should see 8 colour-coded clusters:

| Folder | Colour | What lives here |
|---|---|---|
| `identity/` | 🟧 orange | Profile, research interests, lab context |
| `concepts/` | 🟨 gold | Biology + methodology concepts |
| `paper-notes/` | 🟦 blue | One note per paper in the dashboard library |
| `experiments/` | 🟥 red | Hypothesis notes with council critique inlined |
| `data-notes/` | 🟦 teal | Observations and decisions from data analysis |
| `drafts/` | 🟨 yellow | Manuscript pointers + blog outlines |
| `daily/` | 🟪 purple | Per-session summary notes |
| `inbox/` | ⬜ grey | Quick-capture ideas + meeting notes |

The colour groups are pre-configured in `.obsidian/graph.json`. If they don't appear, refresh via Graph view → settings (gear icon top-right) → Groups.

## 4 · Tour starting points

Most useful entry notes:

- `README.md` — vault gateway, explains the structure.
- `identity/profile-kerem.md` — the researcher's profile (links to interests, lab context).
- `experiments/hyp-cbc-vitals-antibiotic-response.md` — the central hypothesis with full council critique.
- `drafts/manuscript-cbc-antibiotic-response.md` — the manuscript-in-progress pointer.
- `concepts/host-response-paradigm.md` — the framing concept that connects most paper notes.

## 5 · Optional: install useful community plugins

For the demo, the built-in graph view is enough. If you want deeper exploration:

- **Dataview** — query notes by frontmatter
- **Templater** — note templates for new captures
- **Quick Switcher++** — better fuzzy search

Settings → Community plugins → Browse → install.

## 6 · Don't confuse with your personal vault

If you already use Obsidian:

- Your personal vault stays open in the original Obsidian window.
- The workshop vault opens in a **new Obsidian window**.
- Cmd+1 / Cmd+2 (Mac) cycles between open vaults.
- Nothing is shared, copied, or modified across vaults.

## 7 · Vault portability

The vault is just a folder of markdown files. To take a snapshot or share:

```bash
# Snapshot:
tar -czf vault-snapshot.tar.gz ~/Projects/agentic-ai-for-scientists-workshop/week-01-foundations/obsidian-vault/

# Or commit + push (the vault is tracked in this repo)
cd ~/Projects/agentic-ai-for-scientists-workshop
git add week-01-foundations/obsidian-vault/
git commit -m "vault: notes update"
git push
```

Pulling on the second laptop:

```bash
cd ~/Projects/agentic-ai-for-scientists-workshop
git pull
```

If Obsidian is open, the changes appear immediately (it watches the file system).
