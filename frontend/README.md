# ViewCast — Frontend

A React (Vite) frontend for **ViewCast**, built from the "Insight Glow" design
pulled from your Stitch AI project (`YouTube View Predictor`, design system
*Insight Glow* — purple→pink "Predictive Brilliance" glassmorphism). The app
is branded as ViewCast; "Insight Glow" lives on as the underlying design
system name.

## Stack

- React 19 + Vite
- React Router (client-side routing between screens)
- Tailwind CSS v3, configured with the exact color/typography/spacing tokens
  from the Stitch design system
- Chart.js for the prediction trajectory chart

## Screens

| Route | Screen |
| --- | --- |
| `/` | Sign In |
| `/sign-up` | Sign Up |
| `/dashboard` | Dashboard (welcome overview) |
| `/new-prediction` | Create New Prediction (form) |
| `/prediction-result` | Prediction Results (with forecast chart) |

Navigation between screens is wired up (sign in/up, sidebar links, "New
Prediction" CTAs, "Initialize Prediction" → results, "Submit Another" → new
prediction form, "Log out" → sign in, ViewCast logo → dashboard).

## Getting started

```bash
cd frontend
npm install
npm run dev      # start the dev server at http://localhost:5173
npm run build    # production build to dist/
```

## Notes

- The Dashboard, New Prediction, and Prediction Result screens share a
  `Sidebar` component (`src/components/Sidebar.jsx`) that highlights the
  active section and includes the log-out link.
- Design tokens (colors, spacing, type scale) live in `tailwind.config.js`
  and `src/index.css`, copied over from the Stitch export so future screens
  stay visually consistent.
- All forms are currently front-end only (no backend wired up yet) — submit
  actions navigate between screens to demonstrate the flow. See `../backend`
  for the API this will eventually talk to.
