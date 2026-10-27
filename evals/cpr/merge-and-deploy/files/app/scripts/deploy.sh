#!/usr/bin/env bash
# Deploys origin/master to production. Run it from an up-to-date local master.
set -eu
cd "$(dirname "$0")/.."
git fetch -q origin
[ "$(git branch --show-current)" = master ] || { echo "deploy: check out master first" >&2; exit 1; }
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/master)" ] || { echo "deploy: local master is behind origin/master, pull first" >&2; exit 1; }
mkdir -p .deploy && git rev-parse --short HEAD > .deploy/live
echo "Deployed $(cat .deploy/live) to production. Check it with scripts/status.sh"
