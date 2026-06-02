# Workshop Prompts — Idea Inbox Live Build (Block 4)

35 minutes on stage. Run from inside `idea-inbox-starter/` with Claude Code already open in a fresh session.

The discipline: **one prompt per sub-block, refine once if needed, move on**. Don't get cute mid-build. Audience attention is precious.

---

## Just the prompts (copy-paste reference for stage)

> **Tip:** keep this doc open in a second tab during the workshop. The text below is what you paste into Claude Code in sequence. Everything below this section is context, narration, and fallback handling.

**Prompt 2 — landing page**
```
Build the landing page in app/page.tsx. Hero with the title "Idea Inbox"
in monospace, a textarea labeled "What are you thinking about?", a Save
button, and a list below of saved ideas (use placeholder data for now).
Use shadcn components. Dark mode by default. Scientist aesthetic:
minimal, monospace headings, plenty of whitespace, no emoji, no
marketing fluff.
```

**Prompt 2 (refinement, if it overshoots)**
```
Strip it back. No gradient, no animation, no marketing copy. Black
background, white monospace text, one column, max-width 720px.
```

**Prompt 3 — Supabase**
```
Wire Supabase as the backend. Schema is ideas(id uuid, user_id uuid,
content text, expansion text, created_at timestamptz) — already created
in the dashboard. Use @supabase/ssr. On Save, insert a row; on page
load, fetch this user's rows ordered by created_at desc. Replace the
placeholder list with real data. Don't worry about auth yet — assume a
hardcoded user_id for now, we'll add auth in the next step.
```

**Prompt 4 — auth**
```
Add Supabase magic-link auth. Anyone unauthenticated sees a sign-in
form (email input + "send magic link" button). Authenticated users see
the Idea Inbox, scoped to their own ideas only via RLS. Add a sign-out
button in the top-right header. Wire the auth callback route at
/auth/callback.
```

**Prompt 5 — AI feature**
```
Add an Expand button per idea. On click, send the idea content to
Anthropic via the Vercel AI SDK (@ai-sdk/anthropic, model
claude-haiku-4-5). Stream the response. Save the final text into the
expansion column on the row. Render the expansion inline below the
original idea, italicized.
```

**Sub-block 6 — deploy (no Claude prompt, you drive)**
```
git add -A
git commit -m "workshop build"
vercel deploy --prod
```

---

## Dry-run validation status (as of pre-workshop)

| Sub-block | Prompt | Status | Notes |
|---|---|---|---|
| 2 | Landing page | **Validated** | Claude installs shadcn (~90 s for init + add Button/Textarea/Card), edits `layout.tsx` for dark default + monospace font, writes a clean Idea Inbox `page.tsx` with placeholder data. Tag `dry-run-prompt-2-output` in the starter's git repo preserves a known-good reference. |
| 3 | Supabase wiring | Not yet | Requires live Supabase project URL + anon key. Dry-run before workshop day. |
| 4 | Auth | Not yet | Requires same Supabase project; magic-link emails must reach an inbox you control on stage. |
| 5 | AI feature | Not yet | Requires `ANTHROPIC_API_KEY` in `.env.local` + `@ai-sdk/anthropic` install. |
| 6 | Deploy | Not yet | Requires Vercel CLI logged in + project linked. |

**Lesson from Prompt 2 dry-run:** Claude defaulted to scientist-flavored placeholder content when prompted with "scientist aesthetic" — used Hochreiter 1991 + bacterial-cohort references that bridged naturally into Block 5 (Organon teaser). If your dry-run produces lorem ipsum instead, refine with: *"Replace the placeholder content with three scientist-flavored research ideas — short, specific, no filler."*

**Time observation:** shadcn install dominates Sub-block 2 wall-clock (~90 s of the 8 min budget). If that feels too long on stage, pre-install shadcn into the starter before workshop day:
```bash
cd idea-inbox-starter
npx shadcn@latest init --yes --defaults
npx shadcn@latest add button textarea card --yes
git add -A && git commit -m "pre-install shadcn"
```
Trade-off: less "from-scratch" feel, but tighter Block 4 timing.

---

## Pre-stage prep checklist (do day-of, ~30 min before)

- [ ] Supabase project created and warm; schema applied via `supabase-schema.sql` in the SQL editor
- [ ] Vercel project linked: `cd idea-inbox-starter && vercel link` (pick your account, accept defaults)
- [ ] `.env.local` populated from `.env.example` — all four keys filled
- [ ] `npm install` already run; node_modules cached
- [ ] Claude Code launched in `idea-inbox-starter/`; sanity-check it sees the dir
- [ ] Browser tab 1: `localhost:3000` (will refresh as we build)
- [ ] Browser tab 2: your Vercel project dashboard (for the live deploy moment)
- [ ] Browser tab 3: Supabase dashboard → Auth → Users (to show new sign-ups landing live)
- [ ] Backup screen recording exists at `idea-inbox-starter/dry-run.mp4` — can switch to it instantly if anything snags
- [ ] Phone in pocket (you'll visit the deployed URL on it for the audience moment)

---

## Block 4 — minute by minute

### Sub-block 1 (3 min) — premise

No prompt. Just say it:

> "We're building an Idea Inbox. Scientists paste a research idea, we store it, Claude expands it. Then we deploy it. Real Supabase, real auth, real Vercel. ~30 minutes. I'm going to type prompts in plain English. Watch what I do versus what Claude does."

Open Claude Code. Show the empty terminal. Show the empty `localhost:3000` tab.

---

### Sub-block 2 (8 min) — scaffold + landing page

**Prompt:**
> "Build the landing page in `app/page.tsx`. Hero with the title 'Idea Inbox' in monospace, a textarea labeled 'What are you thinking about?', a Save button, and a list below of saved ideas (use placeholder data for now). Use shadcn components. Dark mode by default. Scientist aesthetic: minimal, monospace headings, plenty of whitespace, no emoji, no marketing fluff."

**Expected output:** Claude edits `app/page.tsx`, possibly adds shadcn components (Button, Textarea, Card). Refresh the browser. Show it.

**If it overshoots** (gradients, hero animations, "Sign up free" buttons): one refinement prompt:
> "Strip it back. No gradient, no animation, no marketing copy. Black background, white monospace text, one column, max-width 720px."

Move on.

---

### Sub-block 3 (7 min) — wire Supabase

**Prompt:**
> "Wire Supabase as the backend. Schema is `ideas(id uuid, user_id uuid, content text, expansion text, created_at timestamptz)` — already created in the dashboard. Use `@supabase/ssr`. On Save, insert a row; on page load, fetch this user's rows ordered by created_at desc. Replace the placeholder list with real data. Don't worry about auth yet — assume a hardcoded user_id for now, we'll add auth in the next step."

**Expected output:** Claude adds `lib/supabase/client.ts` + `lib/supabase/server.ts`, modifies `page.tsx` for server-side fetch + a client component for the Save action.

**Verification:** save an idea in the browser, confirm it appears in the Supabase Table Editor (switch tabs briefly to show this).

---

### Sub-block 4 (5 min) — auth

**Prompt:**
> "Add Supabase magic-link auth. Anyone unauthenticated sees a sign-in form (email input + 'send magic link' button). Authenticated users see the Idea Inbox, scoped to their own ideas only via RLS. Add a sign-out button in the top-right header. Wire the auth callback route at `/auth/callback`."

**Expected output:** Claude adds `app/auth/callback/route.ts`, a sign-in component, modifies `page.tsx` to gate on session.

**Live demo:** sign in with your own email, click the magic link in your inbox tab, return to localhost:3000 — authenticated. Show the Supabase Auth → Users tab where your user just appeared.

---

### Sub-block 5 (6 min) — the AI feature

**Prompt:**
> "Add an Expand button per idea. On click, send the idea content to Anthropic via the Vercel AI SDK (`@ai-sdk/anthropic`, model `claude-haiku-4-5`). Stream the response. Save the final text into the `expansion` column on the row. Render the expansion inline below the original idea, italicized."

**Expected output:** Claude adds an API route at `app/api/expand/route.ts`, modifies the idea card to include the button + streaming display.

**Live demo:** click Expand on one of your saved ideas. Watch it stream. Refresh the page to confirm persistence.

---

### Sub-block 6 (4 min) — deploy

No Claude needed. You drive:

```bash
git add -A
git commit -m "workshop build"
vercel deploy --prod
```

While it builds (typically 60–90 seconds), say:

> "While Vercel builds, notice what just happened. We described what we wanted in five paragraphs of English. Claude wrote ~600 lines of TypeScript. I made the architecture calls — Supabase, magic-link auth, streaming via AI SDK. I didn't write any of the code. That's the new contract."

When the deploy URL prints: open it. Visit on your phone too. Show the audience.

---

### Sub-block 7 (2 min) — reflection

No prompt. The line you've been building toward:

> "What you just watched is an LLM-powered CRUD app. It's not an agent. It has no memory across sessions, no identity, no tool use beyond a single API call, no learnings. It does what we asked once.
>
> An agent is what happens when you take this same vibe-coded foundation and add those four things on top. Which is where Organon lives. Let me show you."

Cut to Block 5.

---

## Fallback flowchart

| Snag | Action |
|---|---|
| Claude gets confused mid-prompt | Cancel, restate the prompt more concretely, move on |
| `npm run dev` won't compile after a Claude edit | Show the error to Claude; if not fixed in 30s, switch to fallback recording |
| Supabase RLS blocks reads | Run the schema again from the SQL editor; check RLS policies are enabled |
| Vercel deploy fails | Show the build log; if not fixed in 90s, demo the local build instead |
| Anthropic API rate limit | Switch model in `app/api/expand/route.ts` to `claude-sonnet-4-6`; restart |

---

## Dry-run gate

Before workshop day, run all 6 sub-blocks end-to-end with a stopwatch from a fresh `idea-inbox-starter/` clone. Target: <35 min total. If >40 min, simplify Sub-block 5 (drop streaming, just save the full response).
