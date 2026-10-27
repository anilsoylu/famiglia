#!/usr/bin/env bash
# Prints the commit production is serving.
cd "$(dirname "$0")/.."
echo "production: $(cat .deploy/live 2>/dev/null || echo none)"
