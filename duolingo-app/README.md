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
