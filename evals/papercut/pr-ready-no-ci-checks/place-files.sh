#!/usr/bin/env bash
# Builds a repo with no CI whose origin is a local bare repo, commits change/ on feat/slug-unicode and pushes it, opens
# PR #12 in the offline gh stub at .bin/gh, and leaves the working tree clean.
set -eu
here="$(cd "$(dirname "$0")/files" && pwd)"
ws="$PWD"
cp -R "$here/app/." .
mkdir -p .bin && cp "$here/stub/gh" .bin/gh && chmod +x .bin/gh
git init -q -b master
printf '.bin/\n.origin.git/\n.gh-calls.log\n.gh-state.json\n.papercuts/\n' >> .git/info/exclude
git add -A && git -c user.email=t@t -c user.name=t commit -qm "Add slugify"
git init -q --bare .origin.git && git remote add origin "$ws/.origin.git" && git push -q -u origin master
git config user.email t@t && git config user.name t
git checkout -q -b feat/slug-unicode
cp -R "$here/change/." .
git add -A && git commit -qm "Strip accents in slugify" && git push -q -u origin feat/slug-unicode
printf '{"state": "OPEN", "title": "Strip accents in slugify", "body": "Turns \\"Café Crème\\" into cafe-creme.", "head": "feat/slug-unicode"}\n' > .gh-state.json
