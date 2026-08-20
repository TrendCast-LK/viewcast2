# ViewCast — Frontend

A React (Vite) frontend for **ViewCast**, built from the "Insight Glow" design
pulled from your Stitch AI project (`YouTube View Predictor`, design system
*Insight Glow* — purple→pink "Predictive Brilliance" glassmorphism). The app
is branded as ViewCast; "Insight Glow" lives on as the underlying design
system name.

Talks to the FastAPI backend in `../backend` for real auth, dashboard stats,
and predictions (see **Backend integration** below).

## Stack

- React 19 + Vite
- React Router (client-side routing + route guards)
- Tailwind CSS v3, configured with the exact color/typography/spacing tokens
  from the Stitch design system
- Chart.js for the prediction trajectory chart
- Plain `fetch` for API calls (`src/lib/api.js`) — no extra HTTP library

## Screens

| Route | Screen | Auth required |
| --- | --- | --- |
| `/` | Sign In | – |
| `/sign-up` | Sign Up | – |
| `/dashboard` | Dashboard — real name/subscriber/view stats + recent predictions | ✓ |
| `/new-prediction` | Create New Prediction (form, incl. file upload) | ✓ |
| `/prediction-result/:id` | Prediction Results (real forecast + chart) | ✓ |
| `/trends` | Trends — stat tiles, views-over-time chart, category breakdown | ✓ |
| `/settings` | Settings — edit profile/channel stats, change password | ✓ |

Protected routes redirect to Sign In if there's no session (`RequireAuth` /
`AuthContext`), and back to the page you wanted after logging in.

## Getting started

Needs the backend running first (see `../backend/README.md`).

```bash
cd frontend
npm install
cp .env.example .env   # points at http://localhost:8000 by default
npm run dev             # http://localhost:5173
npm run build            # production build to dist/
```

## Backend integration

- `src/lib/api.js` — thin `fetch` wrapper (`signup`, `login`, `me`,
  `getDashboardSummary`, `createPrediction`, `listPredictions`,
  `getPrediction`, `deletePrediction`), attaches the bearer token, throws
  `ApiError` with a readable message on failure.
- `src/context/AuthContext.jsx` — holds the current user + JWT (persisted to
  `localStorage`), exposes `login`/`signup`/`logout`.
- `src/components/RequireAuth.jsx` — route guard for the pages above.
- New Prediction's file dropzone sends one file, routed server-side to the
  thumbnail or dataset field by MIME type; the two submit buttons hit the
  same endpoint with `save_as_draft` true/false.
- `VITE_API_URL` (in `.env`) points at the backend — change it if the API
  isn't on `localhost:8000`.

## Dark mode

Toggleable from the sun/moon icon in the top bar (every authenticated page)
or the sign-in/sign-up corner, and explicitly from Settings → Appearance.
Defaults to the OS's `prefers-color-scheme` on first visit, then remembers
the explicit choice in `localStorage` (`viewcast_theme`) — applied before
React even mounts (see the inline script in `index.html`) so there's no
flash of the wrong theme on load.

Implementation: every design-system color is a `--color-x: R G B` CSS custom
property (`src/index.css`), with a light table on `:root` and a dark table
under `.dark`; `tailwind.config.js` points each Tailwind color at
`rgb(var(--color-x) / <alpha-value>)` so existing classes (`bg-surface`,
`text-on-background`, `bg-primary/20`, …) work in both themes without
per-component `dark:` variants. `src/context/ThemeContext.jsx` toggles the
`dark` class on `<html>`. Chart.js canvases can't follow CSS variables, so
`src/lib/chartTheme.js` provides matching light/dark color sets and the
chart-owning pages re-create their chart when the theme changes.

## Notes

- The Dashboard, New Prediction, and Prediction Result screens share a
  `Sidebar` component (`src/components/Sidebar.jsx`) that highlights the
  active section and handles log-out.
- Design tokens (colors, spacing, type scale) live in `tailwind.config.js`
  and `src/index.css`, copied over from the Stitch export so future screens
  stay visually consistent.
- The forecast shown on Prediction Results comes from the backend's mock
  forecast engine, not a real ML model yet — see `../backend/README.md`.
