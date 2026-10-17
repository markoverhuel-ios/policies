# Fresh Coast RF, LLC: app policies

Public privacy policies and support pages for our iOS apps, served by GitHub Pages.
**This repo is public. It holds only these HTML pages: no app code, no drafts of unreleased apps, no secrets.**

Site: <https://markoverhuel-ios.github.io/policies/>

## URLs for App Store Connect

| App | Privacy Policy URL | Support URL |
|---|---|---|
| (listed apps appear on the home page) | `https://markoverhuel-ios.github.io/policies/<slug>/privacy.html` | `https://markoverhuel-ios.github.io/policies/<slug>/support.html` |

Tower Roster is set up at `tower-roster/` but is **not listed** yet (it has a TODO for the support email, and its pages carry `noindex` so search engines skip them).

## Add a new app

```sh
./new-app.sh <slug> "<App Name>" <support-email>   # creates <slug>/ from template/, marked noindex
# edit the TODOs in <slug>/privacy.html and <slug>/support.html so they are true for the app
./check.sh <slug>                                  # fails while TODO / placeholders remain
git add -A && git commit -m "Add <App Name> pages" && git push
# when the app is released:
./list-app.sh <slug> "<App Name>"                  # checks, un-hides, adds it to the home page
git commit -am "List <App Name>" && git push
```

Rules for what goes in a policy page:
- It must be true. List every server the app talks to and what is sent.
- Use a role email (support@...), not a personal address: it is public.
- Existing apps (HAMTrainer, grol-trainer, ULS-Dashboard, TaxBracketThermometer) keep their own repos and URLs. Don't move them: Apple has those URLs.

CI runs `./check.sh` on every push and fails if a listed app still has placeholders.

## Layout

- `index.html`: home page (apps appear between the `apps:` markers; edited by `list-app.sh`)
- `assets/style.css`: shared styles, light and dark
- `template/`: starting pages for a new app
- `new-app.sh`, `list-app.sh`, `check.sh`: the three scripts above
