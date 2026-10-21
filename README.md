# Fresh Coast RF, LLC: app pages

Overview, privacy policy and support pages for every Fresh Coast RF iOS app, in one branded site.
**This repo is public. It holds only these HTML pages: no app code, no drafts of unreleased apps, no secrets.**

- Future home: <https://apps.freshcoastrf.com/> (Cloudflare Pages, deploys from `main` on every push)
- Still served by GitHub Pages too: <https://markoverhuel-ios.github.io/policies/>
- Contact on every page: `support@freshcoastrf.com`

## Status: future state, not live for the apps yet

The apps and App Store Connect still point at their old pages, which stay as they are until the brand update ships:

| App | Slug here | Old pages (still live, registered with Apple) |
|---|---|---|
| FRN Dashboard (App Store: ULS Dashboard) | `frn-dashboard` | ULS-Dashboard repo |
| GROL Trainer | `grol-trainer` | grol-trainer repo |
| HAMTrainer | `ham-trainer` | HAMTrainer repo (`docs/`) |
| Spectrum Scout | `spectrum-scout` | spectrum-scout repo |
| Tower Roster (not released, unlisted, `noindex`) | `tower-roster` | this repo: `github.io/policies/tower-roster/` |

At the brand update: change the Privacy Policy URL (any time) and the Support URL (with the next version) in App Store Connect to
`https://apps.freshcoastrf.com/<slug>/privacy` and `https://apps.freshcoastrf.com/<slug>/support`, update the in-app links,
then point the old pages at the new ones. Until then, don't redirect anything.

## Add a new app

```sh
./new-app.sh <slug> "<App Name>" support@freshcoastrf.com   # creates <slug>/ from template/, marked noindex
# edit the TODOs in <slug>/index.html, privacy.html and support.html so they are true for the app
./check.sh <slug>                                           # fails while TODO / placeholders remain
git add -A && git commit -m "Add <App Name> pages" && git push
# when the app is released:
./list-app.sh <slug> "<App Name>"                           # checks, un-hides, adds a card to the home page
git commit -am "List <App Name>" && git push
```

Rules for what goes in a policy page:
- It must be true. List every server the app talks to and what is sent.
- Use the role email (support@freshcoastrf.com), not a personal address: it is public.

CI runs `./check.sh` on every push and fails if a listed app still has placeholders.

## Layout

- `index.html`: home page (app cards sit between the `apps:` markers; edited by `list-app.sh`)
- `<slug>/index.html`, `privacy.html`, `support.html`: each app's three pages
- `assets/style.css`: shared branded styles (Navy #0B2946, Lake Blue #168BBD), light and dark
- `assets/logo.svg`, `favicon.*`: from Company/assets/logo-suite (FCRF_LLC_Horizontal_White, FCRF_Favicon_512)
- `template/`: starting pages for a new app
- `new-app.sh`, `list-app.sh`, `check.sh`: the scripts above
