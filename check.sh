#!/bin/sh
# Fail if an app's pages still have TODOs or placeholder text.
#   ./check.sh [slug ...]   (no args: every app listed on the home page; unreleased apps may still have TODOs)
set -u
bad=0
dirs=$*; [ -n "$dirs" ] || dirs=$(grep -o 'href="[a-z0-9-]*/privacy.html"' index.html | sed 's/href="//; s#/privacy.html"##' | sort -u)
for d in $dirs; do
  for f in "$d"/privacy.html "$d"/support.html; do
    [ -f "$f" ] || { echo "MISSING $f"; bad=1; continue; }
    if grep -n -i -e 'TODO' -e 'FILL IN' -e '{{' -e 'example\.com' "$f"; then echo "  ^ placeholder left in $f"; bad=1; fi
  done
done
[ $bad -eq 0 ] && echo "OK (checked: ${dirs:-none listed})" || { echo "Fix the above before listing or submitting."; exit 1; }
