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
s = open("index.html", encoding="utf-8").read()
import re
tag = re.search(r'<p class="tagline">(.*?)</p>', open(f"{slug}/index.html", encoding="utf-8").read()).group(1)
line = f'<li class="app-card"><img class="app-icon" src="assets/icons/{slug}.png" alt="" width="64" height="64"><div><h2>{name}</h2><p>{tag}</p><div class="links"><a href="{slug}/privacy.html">Privacy</a><a href="{slug}/support.html">Support</a></div></div></li>\n'
if f'href="{slug}/privacy.html"' in s:
    sys.exit("already listed")
s = s.replace("<!-- apps:end -->", line + "<!-- apps:end -->")
open("index.html", "w", encoding="utf-8").write(s)
PY
sed -i.bak 's#<meta name="robots" content="noindex">##' "$slug/index.html" "$slug/privacy.html" "$slug/support.html" && rm -f "$slug"/*.bak
echo "Listed $name."
