# Ultron showcase

Buildless, responsive static website. Open `dist/index.html` directly or serve `dist` with any static web server. No app keys, backend, or dependencies are required. Google Fonts is optional; system font fallbacks are included.

## Preview

```powershell
python -m http.server 4173 --directory dist
```

Visit http://localhost:4173. Deploy the contents of `dist` to a static host.

## Content and assets

- Inspired by the composition of Outcrowd's incident-management website reference supplied by the user: https://dribbble.com/shots/26742281-Website-for-an-Incident-Management-Platform
- Home, Connectors, and Skills images are fresh wireless-ADB captures of the user's installed Ultron 1.8.0 app, captured 6 November 2026. Old README screenshots are not used.
- Features are grounded in the current device UI and repository documentation. Capability examples are clearly illustrative; they do not invoke the assistant.
- Contact CTA opens an email draft addressed to the creator listed in the project README. No email is sent by the site.
- Edit `dist/index.html` for content, `dist/styles.css` for appearance, and `dist/app.js` for capability examples and mobile navigation.

## Motion redesign (6 November 2026)

Reworked against the user-supplied 15-second reference video: layered violet lighting, animated dust, light sweeps, staged scroll reveals, an SVG connection diagram, a varied feature grid, floating product compositions, and a closing light beam. App screenshots retain the original red UI.

Motion uses native CSS and a capped 30-fps canvas loop; the loop stops in hidden tabs. The page honors prefers-reduced-motion and includes a Pause motion button. No scroll hijacking, animation libraries, or runtime dependencies. The reference video is not included in the published assets.

Verified in the browser at 1280px and 390px: navigation, capability selection, FAQs, pause/resume, screenshot loading, and horizontal overflow. JavaScript syntax and asset/anchor integrity checks passed.
