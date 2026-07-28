# Duolingo English App

A small full-stack English-practice app with three activities: grammar
exercises, Hindi-to-English translation, and image comprehension.
Everything runs on static, hand-written content stored in memory — there's
no database and no external AI API, so it needs no API keys and no setup
beyond installing dependencies.

## Stack

- **Backend:** Flask (REST API + serves the built frontend)
- **Frontend:** React + Vite, plain CSS (no Tailwind/UI kit)
- **Content:** in-memory Python data structures in `backend/data.py`
- **Progress tracking:** XP/streak stored in the browser's `localStorage`

## Project structure

```
duolingo-app/
├── backend/
│   ├── app.py            Flask routes (API + static file serving)
│   ├── data.py            All question/sentence/image content, in memory
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/         Home, Grammar, Translation, ImageComprehension
│   │   ├── components/    Topbar
│   │   ├── api.js         fetch wrapper for the Flask API
│   │   └── progress.js    localStorage XP tracker
│   └── package.json
├── build.sh                Builds frontend + installs backend deps (used at deploy time)
├── render.yaml              One-click Render config
└── Procfile                 For Heroku/Railway-style platforms
```

## Running locally

You need Python 3.10+ and Node 18+.

**Backend** (http://localhost:5000):
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend**, in a second terminal (http://localhost:5173, proxies `/api` to the Flask server):
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 while developing. For a production-style single-server run:
```bash
cd frontend && npm run build && cd ..
cd backend && python app.py
```
Then visit http://localhost:5000 — Flask serves the built frontend directly.

## Deploying

This is one deployable service: Flask serves the API under `/api/*` and
the built React app for everything else, so you only need to host one
process. No environment variables or secrets are required.

### Render (recommended, free tier)
1. Push this repo to GitHub.
2. On [render.com](https://render.com), New → Blueprint, point it at your repo.
   It will read `render.yaml` and configure everything automatically.
3. Deploy. Render runs `build.sh` (installs Python deps, builds the
   frontend) then starts `gunicorn app:app`.

### Split deployment: Backend on Render, Frontend on Vercel (recommended)

This repository supports splitting the services: host the backend on Render
and the frontend on Vercel. Benefits: faster static CDN, separate scaling,
easy CI.

1. Push this repo to GitHub.

2. Deploy the backend to Render:
   - New → Web Service → Connect to repo. Render will read `render.yaml`.
   - In the Render dashboard for the service, set an environment variable:
     - `ALLOWED_ORIGINS` — comma-separated list of allowed origins for CORS,
       e.g. `https://your-frontend.vercel.app` (add `http://localhost:5173` for local dev).
   - Deploy. The backend URL will be something like `https://<your-service>.onrender.com`.

3. Deploy the frontend to Vercel:
   - Import the `frontend` folder as a new project (set Root Directory to `frontend`).
   - In Vercel project settings → Environment Variables, add:
     - `VITE_API_BASE` = `https://<your-service>.onrender.com` (no trailing slash).
   - Deploy. Vercel will run `npm run build` and serve the static site.

4. Confirm CORS and connectivity:
   - The backend reads `ALLOWED_ORIGINS` and only accepts requests from the
     origins you list. Add your Vercel domain to `ALLOWED_ORIGINS` on Render.
   - The frontend uses `VITE_API_BASE` at build time to call the API.

Local testing with split setup:

```bash
# Run backend locally
cd backend
pip install -r requirements.txt
gunicorn app:app

# Build frontend using the backend URL
cd ../frontend
npm install
VITE_API_BASE=http://localhost:5000 npm run build
npm run preview
```

Files changed for split deployment:
- `backend/app.py`: CORS locked to `ALLOWED_ORIGINS` env var.
- `backend/requirements.txt`: added `Flask-Cors`.
- `frontend/src/api.js`: reads `VITE_API_BASE` at build time.
- `render.yaml`: backend service definition for Render.

If you want, I can also create a small GitHub Actions workflow to deploy the
frontend to Vercel automatically on push to `main`.

## CI / Auto-deploy (GitHub Actions)

Two workflows are included to auto-deploy on push to `main`:

- `.github/workflows/deploy-frontend-vercel.yml` — builds `frontend` and deploys to Vercel.
- `.github/workflows/trigger-render-deploy.yml` — triggers a Render deploy for the backend using the Render API.

To use these workflows, add the following GitHub repository secrets (Repository → Settings → Secrets):

- `VERCEL_TOKEN` — a Vercel Personal Token (create via Vercel Dashboard).
- `VERCEL_ORG_ID` — your Vercel Organization or Team ID (found in Vercel project settings).
- `VERCEL_PROJECT_ID` — the Vercel Project ID for the `frontend` project.
- `RENDER_API_KEY` — a Render API key with `deploy` scope (create in Render Dashboard).
- `RENDER_SERVICE_ID` — the Render Service ID for your backend service (found in the service settings URL or Render Dashboard).

Notes:
- The Vercel action used here (`amondnet/vercel-action`) requires the three Vercel secrets above. If you prefer Vercel Git integration (recommended), you can skip the Vercel token secrets — Vercel will auto-deploy on pushes after you connect the repo in their UI.
- The Render workflow simply calls the Render Deploys API; Render will use `render.yaml` from the repo to perform the build. Alternatively, you can enable Render's native GitHub integration (recommended) and skip the `RENDER_API_KEY`/`RENDER_SERVICE_ID` secrets.

If you want, I can help create the GitHub Secrets values and test a push, but I need access tokens/permissions to do that.

### Railway / Heroku-style platforms
The included `Procfile` works out of the box. Set the build command to
`bash build.sh` (or equivalent buildpack step) if the platform doesn't
auto-detect it.

### Any other host that runs Python
```bash
bash build.sh
cd backend
gunicorn app:app --bind 0.0.0.0:$PORT
```

## Notes

- Content (grammar questions, translation sentences, image prompts and
  their reference descriptions) lives entirely in `backend/data.py`.
  Add more entries there to grow the question bank — no other code
  changes needed.
- Images are loaded from picsum.photos (public, keyless) by fixed ID, so
  the same handful of images always pair with their hand-written
  reference descriptions and keyword lists.
