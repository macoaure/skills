---
name: gitmoji-changelog
description: Generates or updates a project's CHANGELOG.md (or .json) straight from its gitmoji-prefixed git history, using the gitmoji-changelog CLI (https://github.com/frinyvonnick/gitmoji-changelog) run inside Docker so no global npm/Node install is required on the host. Sorts commits into Keep a Changelog style sections (Added, Changed, Breaking changes, Removed, Fixed, Security, Misc) purely from each commit's gitmoji, and can build the full history from tags or just append commits made since the last recorded version. Use this whenever the user asks to generate, build, update, or regenerate a changelog, release notes, or CHANGELOG.md — especially for a repo whose commits already use gitmoji — even if they don't mention Docker or the tool by name. Pairs naturally with the gitmoji-commits skill, since commits that skill writes are already in the exact shortcode form this tool parses.
---

# Gitmoji Changelog

`gitmoji-changelog` walks a repo's git history, finds every commit whose subject starts with a
gitmoji (as a `:shortcode:` or the literal emoji — it converts between the two internally), and
sorts each one into a changelog section based purely on which gitmoji it used. The sections and
exactly which gitmoji falls into which one are fixed by the tool itself, not configurable
per-run — see `references/changelog-sections.md` for the full table, transcribed from the
project's own source, so you can tell the user ahead of time where a commit will land instead of
only finding out after generating the file.

A commit using an unrecognized-but-still-gitmoji subject doesn't get silently dropped — it falls
into "Miscellaneous" as a catch-all. The one real exception is `:bookmark:` (release/version tag
commits), which the tool filters out of the changelog entirely as noise, not just hides.

## Why Docker

The tool is an npm package, so the obvious way to run it is `npx gitmoji-changelog`. This skill
runs it through Docker instead, for one reason: `npx` would pull whatever the *latest* published
version happens to be at the moment you run it, so the same command can behave differently next
month if upstream ships a breaking release — and this skill's instructions (which sections exist,
which flags are available) are written against one specific version. Baking that version into a
Docker image means the behavior documented here is the behavior you actually get, indefinitely,
without the skill needing to be re-verified every time upstream publishes.

`docker/Dockerfile` pins `gitmoji-changelog@2.3.0` on a small `node:20-alpine` base with `git`
installed (the tool shells out to the real `git` binary to read commits and tags, so that's a
hard requirement, not an extra). `scripts/gitmoji-changelog.sh` builds that image on first use
(cached after that) and then runs it, mounting whatever directory you call it from into the
container at `/app` — which doubles as both the image's `WORKDIR` and where the tool expects to
find the target repo's `.git` folder and project manifest.

This has been run end to end against a real repo (building the image, generating a changelog,
reading the result). Two things about the container needed fixing along the way, both already
baked into `docker/Dockerfile` and `scripts/gitmoji-changelog.sh`:

- Git refuses to touch a repo it doesn't own ([CVE-2022-24765](https://github.blog/open-source/git/git-security-vulnerability-announced/)'s "dubious ownership" check) —
  the container runs as root while the bind-mounted repo is owned by the host user, so the image
  marks `/app` as a `safe.directory` for git up front.
- Any unhandled error (not just that one) makes the CLI try to copy a GitHub issue report to the
  clipboard via `xsel`, which doesn't exist in this headless image and crashes with a confusing
  secondary error that hides the real one. Setting `CI=true` on the container takes a plain-text
  branch instead, so the actual error (if any) stays visible on stdout.

## Workflow

### 1. Confirm Docker is available

Run `docker info`. If it fails, Docker Desktop (or the daemon) isn't running — ask the user to
start it rather than silently falling back to a host `npx` install, since that would skip the
whole point of pinning a version.

### 2. Figure out the project's preset

This step is mandatory, not optional setup — if the active preset can't resolve project info,
the CLI silently produces nothing at all (see Caveats below), so get this right before running
anything. Don't stop to ask the user for this, though — everything needed is either already
sitting in the repo or has a reasonable inferred default, and blocking on a question here would
turn an otherwise one-shot workflow into a back-and-forth for no real benefit to the user.

Run `scripts/ensure_project_config.py <repo_root>` and use whatever `preset=` it prints:

- If the repo already has a `package.json`, `pom.xml`, `Cargo.toml`, or `Chart.yaml`, the script
  reports the matching preset (`node`/`maven`/`cargo`/`helm`) and leaves everything alone — that
  manifest is already all gitmoji-changelog needs. (There's no `python` preset here — the
  upstream repo's current source has one, but the pinned `2.3.0` release this skill runs does
  not; its own `--help` only lists `node, generic, maven, cargo, helm`. A Python project without
  a `package.json` falls through to the generic branch below, which works fine.)
- Otherwise it auto-generates a `.gitmoji-changelogrc` for `--preset generic`, inferring
  `name` from the git remote (falling back to the directory name), `description` from the first
  real line of `README.md` (falling back to a generic placeholder), and `version` from the
  latest git tag with any leading `v` stripped (falling back to `0.0.0` if there are no tags
  yet). It never overwrites a `.gitmoji-changelogrc` that's already there, in case a human tuned
  it by hand.
- Mention the file and the values it chose when you report back — the user should know it exists
  and what's in it, even though nothing blocked on their input to create it. If `version` landed
  on the `0.0.0` fallback and that's clearly wrong for the project, it's worth a quick note so
  they can edit the file before the next run, rather than something to interrupt this run over.

### 3. Decide init vs. update

- **No `CHANGELOG.md` yet**: run `init`. This walks every git tag in the repo and builds a full
  version-by-version changelog in one pass.
- **`CHANGELOG.md` already exists**: the plain (no-subcommand) form of the CLI auto-detects this
  and only adds commits made since the last version already recorded in the file — the explicit
  `update [release]` form does the same thing by name, if you want to be unambiguous about it.
- **The `[release]` argument** (works with the default command and `update`) is the label for
  the version being generated: `from-package` (default — pulls the version from whichever preset
  is active), `next` (an "Unreleased"-style bucket that doesn't require a matching git tag to
  exist), or an explicit semver string like `2.4.0`.

### 4. Run it

From the root of the target repo (the one with the `.git` folder you want history from):

```bash
/path/to/gitmoji-changelog/scripts/gitmoji-changelog.sh init
/path/to/gitmoji-changelog/scripts/gitmoji-changelog.sh update next
```

Useful flags: `--format json` writes machine-readable JSON instead of markdown; `--output <path>`
changes where the file is written (defaults to `./CHANGELOG.md`, or `./CHANGELOG.json` with
`--format json`). Skip `--author` — it's documented in `--help` but confirmed to be a no-op in
the pinned `2.3.0` release (an A/B run with and without it produced byte-identical output); don't
tell a user it'll add authorship to the changelog.

Skip `--interactive`/`-i` — it pauses the CLI to let someone hand-pick commits from a terminal
prompt, which needs a real TTY and doesn't fit a workflow this skill drives unattended. If the
user wants to curate what made it in, do that by editing the generated file afterward instead.

### 5. Show the result

Don't just report "done" — show the user the new or changed section of `CHANGELOG.md`. It's a
file they're about to commit, so they should see what actually landed in it, including anything
that surprisingly ended up in Miscellaneous because its gitmoji wasn't one of the specifically
sorted ones.

## A note on commits written by gitmoji-commits

The parser reads everything after the first `:shortcode:` match as the changelog line's message
— it doesn't know or care about the conventional-commit `type(scope):` that the gitmoji-commits
skill also puts there. So a commit like `:sparkles: feat(auth): add OAuth login support` shows up
in the changelog as "feat(auth): add OAuth login support" under **Added** — the type/scope prefix
rides along as part of the text. That's expected, not a bug to fix; it reads fine as an inline
label, just mention it if a user seems surprised by it.

## Caveats

- **No project info means no changelog at all, and it fails silently-ish.** If the active preset
  can't find what it needs — `node` with no `package.json` anywhere up the directory tree, or
  `generic` with no `.gitmoji-changelogrc` — the CLI logs `Cannot retrieve configuration for
  preset <preset>.` and exits **with code 0**, not a failure code. It does not fall back to
  guessing or to another preset. This means step 2 (confirm a preset's project info actually
  resolves) isn't optional busywork — skip it and the tool can "succeed" from a script's point
  of view while writing nothing. Always check the CLI's own output text for that "Cannot
  retrieve configuration" line rather than trusting the exit status.
- Needs at least one commit reachable from `HEAD`. Running `init` against a brand-new, empty
  repo fails with "No changes found" rather than producing an empty file.
- `git-raw-commits`/`git-semver-tags` (the tool's underlying git access) need the repo's full
  history and tags available in the mounted directory — a shallow clone (`git clone --depth 1`)
  will produce an incomplete or empty changelog.
