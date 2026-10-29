#!/usr/bin/env bash
# Builds the pinned gitmoji-changelog image on first use, then runs it against
# the current directory. Usage mirrors the real CLI exactly:
#   gitmoji-changelog.sh [init | update [release]] [options]
set -euo pipefail

IMAGE="gitmoji-changelog:2.3.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKERFILE_DIR="$SCRIPT_DIR/../docker"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Building $IMAGE (first run only, cached after this)..." >&2
  docker build -t "$IMAGE" "$DOCKERFILE_DIR"
fi

# Mount the current directory (must be the repo root, with its .git folder)
# at /app, which is the image's WORKDIR and where gitmoji-changelog looks for
# both the git history and the project manifest / .gitmoji-changelogrc.
#
# CI=true matters for any internal error, not just one specific one: on any
# unhandled exception the CLI tries to generate a GitHub issue report and,
# outside a detected CI environment, copies it to the clipboard via `xsel` --
# which doesn't exist in this headless image and crashes instead of printing
# a usable error message. CI=true takes env-ci's plain-text-link branch
# instead, so whatever actually went wrong is still visible on stdout.
docker run --rm -e CI=true -v "$(pwd)":/app "$IMAGE" "$@"
