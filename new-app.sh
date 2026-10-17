#!/bin/sh
# Add a new app to this site.
#   ./new-app.sh <slug> "<App Name>" <support-email>
# Example: ./new-app.sh tower-roster "Tower Roster" support@example.com
# Creates <slug>/privacy.html and <slug>/support.html from template/. The app is NOT listed on the
# home page until you run ./list-app.sh, so nothing public links to it before it is released.
set -eu
[ $# -eq 3 ] || { echo "usage: $0 <slug> \"<App Name>\" <support-email>"; exit 1; }
slug=$1; name=$2; email=$3
case $slug in *[!a-z0-9-]*|"") echo "slug must be lowercase letters, digits and dashes"; exit 1;; esac
[ ! -e "$slug" ] || { echo "$slug already exists"; exit 1; }
company="Fresh Coast RF, LLC"; date=$(date "+%B %Y")
mkdir "$slug"
for f in privacy support; do
  python3 - "$f" "$slug" "$name" "$company" "$email" "$date" <<'PY'
import sys
f, slug, name, company, email, date = sys.argv[1:]
s = open(f"template/{f}.html").read()
for k, v in {"APP_NAME": name, "COMPANY": company, "EMAIL": email, "DATE": date}.items():
    s = s.replace("{{" + k + "}}", v)
s = s.replace("<head>", "<head><meta name=\"robots\" content=\"noindex\">", 1)
open(f"{slug}/{f}.html", "w").write(s)
PY
done
echo "Created $slug/. Edit the TODOs in $slug/privacy.html and $slug/support.html, then run ./check.sh"
echo "When the app is released: ./list-app.sh $slug \"$name\""
