# GenAI Foundations for Scientists — Week 1 Workshop Materials

Workshop materials for the first session of the *Agentic AI for Scientists* series.

## What's in here

| File / dir | Purpose |
|---|---|
| `brief.md` | Locked plan — goal, deliverables, acceptance criteria, timeline, risks |
| `slides.md` | Marp deck (drafted in a later step) |
| `slides.pdf` / `slides.pptx` | Exported deck for projector + screen-share fallback |
| `talk-notes.md` | Per-block speaker notes |
| `WORKSHOP_PROMPTS.md` | The 6 prompts to run live during Block 4, timed |
| `supabase-schema.sql` | Schema + RLS policies for the `ideas` table |
| `.env.example` | Placeholder env vars (Supabase + Anthropic) |
| `idea-inbox-starter/` | Empty Next.js + shadcn + Tailwind shell — opens to localhost:3000 |
| `dry-run.mp4` | Backup recording of the full live build (record this once, before workshop day) |

## Pre-workshop dry-run flow

Do this once, ~24h before the workshop.

```bash
# 1. Fresh clone of the starter
cd projects/briefs/agentic-ai-workshop/idea-inbox-starter

# 2. Verify boot
npm install
npm run dev
# → open http://localhost:3000, confirm empty page renders

# 3. Apply Supabase schema
# Supabase dashboard → SQL Editor → paste supabase-schema.sql → Run

# 4. Fill in .env.local
cp ../.env.example .env.local
# fill in: SUPABASE_URL, SUPABASE_ANON_KEY, ANTHROPIC_API_KEY

# 5. Link Vercel
vercel link

# 6. Walk through WORKSHOP_PROMPTS.md with a stopwatch
# Target: <35 min total. If >40 min, simplify Sub-block 5.

# 7. Record the dry-run for fallback
# Use QuickTime or OBS; save as dry-run.mp4 next to this README
```

## On stage

1. Open Claude Code in `idea-inbox-starter/`
2. Open the three browser tabs from `WORKSHOP_PROMPTS.md` prep checklist
3. Run prompts 1 → 6 in order
4. If anything snags >30 seconds, switch to `dry-run.mp4`

## Voice rules

The build is a CRUD app, not an agent. Block 4 narration must say "LLM-powered app" or "vibe-coded tool" — never "agent". The contrast between this build and Organon (Block 5) is the bridge to the rest of the series.
