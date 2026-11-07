# Ultron website

Static site for Ultron, a voice assistant for Android. Live at https://ultron.devxjitin.dev

Everything the site serves is in `dist/` (plain HTML, CSS and JS, no build step). Pushing to `main` deploys it with GitHub Actions.

Pages: `index.html` (features, pricing, install guide, FAQ, support), `privacy.html` and `terms.html`.

Plans and prices (Spark 7 days ₹199, Surge 1 month ₹699, Apex 3 months ₹1,499) are written in the pricing section of
`index.html` and in section 1 of `terms.html`. Keep them the same as `PLANS` in `ultronapp/app.js`.

The Buy buttons open an email to devxjitin@gmail.com. To send orders to WhatsApp instead, set `BUY_WHATSAPP` at the end of
`app.js` (country code first, digits only, for example `919876543210`); the buttons and a WhatsApp card under Support switch
over by themselves.

Preview locally: `python -m http.server 4173 --directory dist`
