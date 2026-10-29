# skills

Personal collection of [Claude Code](https://claude.com/claude-code) skills.

## Skills

- [`gitmoji-commits`](./skills/gitmoji-commits) — plans and executes git commits using the
  [gitmoji](https://gitmoji.dev) + [conventional commits](https://www.conventionalcommits.org)
  pattern. Splits a messy working-tree diff into small, specific, logical commits, picks the
  right gitmoji shortcode and matching commit type from a fixed mapping, and runs each commit
  after confirming the plan.

## Install

Install any skill from this repo with the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add macoaure/skills --skill gitmoji-commits
```

Add `-g` to install it globally instead of just the current project, or `-a <agent>` to target
a specific agent (e.g. `-a claude-code`). Omit `--skill` to pick interactively from everything
in this repo. See `npx skills --help` for the full set of options.

### Manual install

Alternatively, clone or symlink a skill's directory into your Claude Code skills folder
(typically `~/.claude/skills/`):

```bash
git clone https://github.com/macoaure/skills.git /tmp/macoaure-skills
cp -r /tmp/macoaure-skills/skills/gitmoji-commits ~/.claude/skills/gitmoji-commits
```
