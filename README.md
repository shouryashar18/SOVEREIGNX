# SIH26171 — Screens

One Vite + React app that wires together all 22 Stitch-exported screens from
`sih-frontend` so they run as a single site instead of 22 disconnected HTML
files.

## Run it

```bash
npm install
npm run dev
```

Then open the printed local URL. You'll get:

- A home grid of every screen with a thumbnail
- A sidebar grouped by area (Core, Auth & Onboarding, Agents, Monitoring, Admin, Industry Views)
- Click any screen to open it in the viewer, or "Open in new tab" for a full-page view

## How it's wired

Each screen keeps its **original HTML/CSS exactly as exported** (own Tailwind
CDN import, own color config, own fonts) — they live untouched under
`public/pages/<slug>/index.html` and render inside an `<iframe>` at
`/#/screen/<slug>`. This avoids breaking each screen's bespoke palette, which
differs screen to screen and isn't a shared design system yet.

The React shell (`src/App.jsx`, `src/pages.js`, `src/App.css`) only provides:
navigation, routing, and the home grid — it doesn't touch the screens' own
markup or styling.

## Known gaps

- `cyber_industrial_intelligence/` and `obsidian_command/` in the original
  repo only contained a `DESIGN.md` brief, no built HTML — they're not in
  the nav. Build those screens and drop a `code.html` (renamed to
  `index.html`) into a new `public/pages/<slug>/` folder, then add an entry
  to `src/pages.js` to wire them in.
- Screens don't share state or navigate to each other yet (e.g. clicking
  "Login" inside the auth screen won't route anywhere in-app) — each is
  still an isolated static page. Turning these into real React
  components with shared layout/router links is the next step if you want
  actual cross-screen flows instead of a screen gallery.

## Deploying

`npm run build` outputs a static site in `dist/` — deployable to Vercel,
Netlify, GitHub Pages, etc. as-is.
