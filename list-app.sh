#!/bin/sh
# List a released app on the home page.   ./list-app.sh <slug> "<App Name>"
set -eu
[ $# -eq 2 ] || { echo "usage: $0 <slug> \"<App Name>\""; exit 1; }
slug=$1; name=$2
[ -f "$slug/privacy.html" ] || { echo "$slug/privacy.html not found"; exit 1; }
./check.sh "$slug"
python3 - "$slug" "$name" <<'PY'
import sys
slug, name = sys.argv[1:]
s = open("index.html").read()
line = f'<li><strong>{name}</strong>: <a href="{slug}/privacy.html">Privacy</a> · <a href="{slug}/support.html">Support</a></li>\n'
if f'href="{slug}/privacy.html"' in s:
    sys.exit("already listed")
s = s.replace("<!-- apps:end -->", line + "<!-- apps:end -->")
open("index.html", "w").write(s)
PY
sed -i.bak 's#<meta name="robots" content="noindex">##' "$slug/privacy.html" "$slug/support.html" && rm -f "$slug"/*.bak
echo "Listed $name."
