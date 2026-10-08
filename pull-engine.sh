#!/usr/bin/env bash
# Pull a tagged engine (the method) into this instance. Run from the instance root:
#
#   ./pull-engine.sh v0.1            # refuses if you edited an engine file here
#   ./pull-engine.sh v0.1 --force    # overwrite local edits to engine files
#
# Copy only, no transforms. Engine-owned files (listed in engine.manifest) are replaced, files the
# new engine dropped are deleted, and starter files in _shared/ are added only if missing. Your
# _shared/ content and runs are never touched. Nothing is committed — review with `git status`.
#
# Override the source with ENGINE_REPO=<url or local path>.
#
# Everything is inside main() so bash parses the whole script before running it: the pull can
# replace this very file, and bash reads scripts lazily.
set -euo pipefail

main() {
  cd "$(dirname "$0")"

  local tag="${1:-}"
  [ -n "$tag" ] || { echo "usage: ./pull-engine.sh <tag> [--force]" >&2; exit 2; }
  local force=""
  [ "${2:-}" = "--force" ] && force="--force"
  local repo="${ENGINE_REPO:-https://github.com/JamesDylan/discovery-pipeline.git}"

  local tmp
  tmp="$(mktemp -d)"
  trap 'rm -rf "'"$tmp"'"' EXIT

  git -c advice.detachedHead=false clone --quiet --depth 1 --branch "$tag" "$repo" "$tmp/engine"
  # use the incoming engine's own installer, so a new tag can change how it installs
  python3 "$tmp/engine/_eval/manifest.py" install "$tmp/engine" "$PWD" ${force:+"$force"}

  echo "Review: git status && ./eval"
}

main "$@"; exit
