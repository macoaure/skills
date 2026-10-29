---
name: gitmoji-commits
description: Plans and executes git commits using the gitmoji + conventional-commits pattern — surveys the full working-tree diff, splits it into multiple small, specific, logical commits instead of one big dump, picks the right gitmoji shortcode (plain text like ":sparkles:", never the rendered emoji character) and matching conventional-commit type for each one from a fixed static mapping, confirms the plan with the user, then stages and runs each commit in order. Use this whenever the user asks to commit changes, split a diff into commits, clean up or organize commits, write a commit message, or mentions gitmoji, conventional commits, or semantic commits — even if they just say "commit this" or "commit my changes" without naming any of those terms explicitly.
---

# Gitmoji Commits

A commit history is read far more often than it's written. One commit per unrelated change,
each labeled with what kind of change it is, turns `git log` into a map of the project's history
instead of a pile of "fixed stuff" messages. This skill plans that history before touching
anything, then carries out the plan.

Two conventions, combined into one commit message:

- **Gitmoji** (https://gitmoji.dev) marks *what kind* of change this is, at a glance, using a
  short textual code like `:sparkles:` or `:bug:`.
- **Conventional commits** marks the same thing in the format tooling (changelogs, semantic-release,
  commitlint) actually parses: `type(scope): subject`.

Combined: `:gitmoji: type(scope): subject` — e.g. `:sparkles: feat(auth): add OAuth login support`.

Always write the shortcode as plain text — `:sparkles:`, not ✨. The shortcode already *is*
gitmoji's own convention (GitHub and GitLab render it as the emoji automatically in their UI),
so nothing is lost by typing it out, and the raw message stays plain text that's safe to grep,
diff, and read in any terminal. **Never paste the literal emoji character into a commit message.**

## The gitmoji → type mapping is fixed, not a judgment call

Read `references/gitmoji-types.md` before building a plan — it's the full static gitmoji catalog
(75 entries), each pinned to exactly one conventional-commit type. Don't improvise a type for a
gitmoji based on context; several of them could plausibly read as more than one type (`:zap:`
could feel like "fix" or "perf"), and if the type floated per-commit, the same *kind* of change
would get labeled inconsistently across the history. Use the table's answer every time.
`scripts/validate_commit.py` checks a message against this same table mechanically — run it on
each planned message before committing, so a mismatch gets caught before it's permanent:

```
python3 scripts/validate_commit.py ":sparkles: feat(auth): add OAuth login support"
```

## Workflow

### 1. Survey the full change set

Don't look at one file or one hunk in isolation — look at everything that could go into a commit
right now: `git status` for an overview, `git diff` for unstaged changes, `git diff --staged` for
anything already staged, and the untracked files `git status` lists. If anything is already
staged, that's a signal of the user's own intent — fold it into the plan rather than silently
restaging everything from scratch.

Stop and flag rather than planning around it if you see: merge-conflict markers, a file that
looks like a secret or credential (`.env`, private keys, tokens), or a binary/generated file that
doesn't belong in version control. These are worth a quick check-in with the user, not a silent
commit.

### 2. Group changes into logical commits

This is the part worth the most thought. The goal is commits that are **numerous and specific**
rather than a few broad ones — each commit should be a single coherent idea that could be
described in one short sentence and, ideally, reverted on its own without dragging unrelated
changes with it. Group by *intent*, not by file:

- Several files that together implement one feature → one commit.
- One file that happens to contain two unrelated edits (say, a bug fix and an unrelated
  formatting pass) → split it with `git add -p`, which lets you stage individual hunks rather
  than the whole file. Don't let "it's all in one file" become an excuse to lump unrelated
  changes into one commit.
- A dependency bump that was needed to ship a feature → usually its own `:arrow_up:` commit
  before the feature commit, so the feature diff doesn't get buried in lockfile noise.
- Pure renames/moves with no logic change → their own `:truck:` commit, so the diff that follows
  is a clean content change instead of a rename-plus-edit that's hard to review.

If you genuinely can't tell whether two edits belong together, lean toward splitting — a reviewer
can always squash commits that turn out to be too granular, but can't un-squash a commit that
buried two unrelated ideas together.

### 3. Write each message

For each group, pick the single gitmoji from `references/gitmoji-types.md` whose description
best matches the change, then use the type that row is pinned to:

```
:shortcode: type(scope): subject
```

- **subject**: imperative mood, lowercase, no trailing period — "add", not "Added" or "Adds".
  Keep the first line to 72 characters or fewer.
- **scope**: optional. Use it when it adds real information (a package name, a directory, a
  module) — `feat(auth):` beats a bare `feat:` when the repo has more than one obvious area.
  Skip it when every commit would get the same scope anyway.
- **body**: every commit gets one. The subject line only has room to say *what* changed; the
  body is where *why* lives — what problem this solves, what prompted it, what approach was
  rejected and why, what the reader needs to know that isn't visible in the diff itself. That
  context is exactly what's expensive to reconstruct later from `git blame` or a stale memory,
  and cheap to write down now while it's still in your head. A couple of sentences is enough —
  this isn't a changelog entry, it's the answer to "why does this line exist" for whoever reads
  it next. A `:boom:` commit additionally needs a `BREAKING CHANGE:` footer describing what
  breaks and, if possible, how to migrate.

  ```
  :sparkles: feat(auth): add OAuth login support

  Password-only login was blocking the SSO rollout the infra team needs by
  end of quarter. Added the OAuth flow alongside the existing password path
  rather than replacing it, since several internal tools still depend on
  password auth for service accounts.
  ```

### 4. Check the plan against the checklist

Before showing the plan to the user, run it against every rule below. A plan that's wrong in
structure (files double-booked into two commits, a dependency bump landing after the feature
that needs it) is much cheaper to fix now than after three commits are already made and later
ones build on the broken ordering.

**Per commit:**

- [ ] First line matches `:shortcode: type(scope): subject` exactly — run
      `scripts/validate_commit.py` on it to confirm the shortcode is real and its type matches
      the fixed table, rather than eyeballing it.
- [ ] Subject is imperative, starts lowercase, has no trailing period, and is 72 characters or
      fewer.
- [ ] Body is present and states *why*, not just a rewording of the subject — "needed for the
      SSO rollout deadline" passes, "adds OAuth support" (just restating the subject) doesn't.
- [ ] The files/hunks assigned to this commit are one coherent idea — if you can't summarize why
      two of them are in the same commit in a single clause, they probably aren't.
- [ ] Nothing staged for this commit is a secret, credential, or generated/binary file that
      doesn't belong in version control.
- [ ] If the gitmoji is `:boom:`, the body has a `BREAKING CHANGE:` footer.

**Across the whole plan:**

- [ ] Every changed file (tracked and untracked, already-staged or not) is covered by exactly
      one commit in the plan — nothing left for "later," nothing claimed by two commits at once.
- [ ] Commits that depend on each other are ordered correctly — a dependency bump or a rename
      comes *before* the commit that relies on it, not after.
- [ ] No two commits in the plan have the same message — if they do, they're either actually one
      commit or need subjects specific enough to tell them apart.
- [ ] The plan has more than one commit unless the change set genuinely is a single idea — a plan
      that lumps everything into one commit defeats the point of planning at all.

If anything on this list fails, fix the plan — regroup, reorder, or rewrite the message — before
moving on. Don't present a plan you know fails one of these.

### 5. Confirm the plan before touching git

Show the full plan as a numbered list — each commit's message plus which files or hunks go into
it — and get a go-ahead before staging or committing anything. Local commits are easy to amend or
reset, but regrouping *is not* once several commits are already made and later ones have started
building on earlier ones, so it's worth getting the grouping right up front rather than fixing it
after the fact.

### 6. Execute in order

For each planned commit, in sequence:

1. Stage exactly what that commit needs — `git add <files>` for whole files, `git add -p` when a
   file's hunks are split across commits.
2. Run `git status` to confirm only the intended changes are staged before committing — this is
   the moment a stray file from the next commit would show up.
3. Optionally sanity-check the message with `scripts/validate_commit.py` first.
4. Commit with the subject and body as separate `-m` flags (git joins them with a blank line),
   or a heredoc for anything longer:
   `git commit -m ":sparkles: feat(auth): add OAuth login support" -m "Password-only login was..."`

After the last commit, run `git log --oneline -n <count>` and show the user the resulting history.

## Edge cases

- **Nothing to commit**: say so plainly rather than inventing a commit. An empty working tree
  isn't a problem to solve.
- **Changes don't split cleanly**: if two edits are too entangled to separate (e.g. a rename that
  also changes behavior in the same lines), it's fine to land them as one commit — just pick the
  gitmoji for the more significant of the two changes and mention the trade-off in the body.
- **Working tree isn't a git repo yet**: offer to `git init` rather than assuming.
- **Already on a branch mid-rebase/merge**: check `git status` for that state before planning
  anything; committing partway through a rebase has different semantics than a normal commit.
