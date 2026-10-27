#!/usr/bin/env bash
set -eu
here="$(dirname "$0")/files"
cp -R "$here/app/." .
git init -q -b master && git add -A && git -c user.email=t@t -c user.name=t commit -qm "base"
[ -d "$here/change" ] && git checkout -q -b feat/team-members && cp -R "$here/change/." . || true
