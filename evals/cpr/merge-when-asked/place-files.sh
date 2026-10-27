#!/usr/bin/env bash
# Builds a repo whose origin is a local bare repo, with an offline gh stub at .bin/gh, and leaves change/ uncommitted
# on feat/team-members.
set -eu
here="$(cd "$(dirname "$0")/files" && pwd)"
ws="$PWD"
cp -R "$here/app/." .
mkdir -p .bin && cp "$here/stub/gh" .bin/gh && chmod +x .bin/gh
git init -q -b master
printf '.bin/\n.origin.git/\n.gh-calls.log\n.gh-state.json\n' >> .git/info/exclude
git add -A && git -c user.email=t@t -c user.name=t commit -qm "Add team lookup endpoint"
git init -q --bare .origin.git && git remote add origin "$ws/.origin.git" && git push -q -u origin master
git config user.email t@t && git config user.name t
git checkout -q -b feat/team-members
cp -R "$here/change/." .
