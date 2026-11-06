# Ultron website

Static site for Ultron, a voice assistant for Android. Live at https://ultron.devxjitin.dev

Everything the site serves is in `dist/` (plain HTML, CSS and JS, no build step). Pushing to `main` deploys it with GitHub Actions.

Preview locally: `python -m http.server 4173 --directory dist`
