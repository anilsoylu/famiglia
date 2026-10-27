#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/app/." .
git init -q -b master && git add -A && git -c user.email=t@t -c user.name=t commit -qm "base"
