#!/usr/bin/env bash
set -eu
here="$(dirname "$0")/files"
cp -R "$here/app/." .
git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm "base"
