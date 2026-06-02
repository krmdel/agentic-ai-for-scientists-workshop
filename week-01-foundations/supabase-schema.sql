-- Idea Inbox schema
-- Apply via Supabase dashboard: Project → SQL Editor → New query → paste → Run

create table if not exists public.ideas (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  content text not null,
  expansion text,
  created_at timestamptz not null default now()
);

create index if not exists ideas_user_id_created_at_idx
  on public.ideas (user_id, created_at desc);

alter table public.ideas enable row level security;

drop policy if exists "users select own ideas" on public.ideas;
create policy "users select own ideas" on public.ideas
  for select using (auth.uid() = user_id);

drop policy if exists "users insert own ideas" on public.ideas;
create policy "users insert own ideas" on public.ideas
  for insert with check (auth.uid() = user_id);

drop policy if exists "users update own ideas" on public.ideas;
create policy "users update own ideas" on public.ideas
  for update using (auth.uid() = user_id);

drop policy if exists "users delete own ideas" on public.ideas;
create policy "users delete own ideas" on public.ideas
  for delete using (auth.uid() = user_id);
