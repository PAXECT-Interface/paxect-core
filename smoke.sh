#!/usr/bin/env bash
set -e
echo -n "smoke" | paxect encode | paxect decode | diff -u - <(echo -n "smoke")
echo "✅ PAXECT CLI smoke OK"
