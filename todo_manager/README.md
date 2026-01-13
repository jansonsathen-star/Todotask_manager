Todo Manager — High-level architecture and frontend notes

Overview

This project is a small Todo application built with Django as the backend and a lightweight React frontend loaded from CDN inside templates. The goal is a SPA-like user experience without a full separate build pipeline.

Architecture (high level)

- Backend: Django (views + models)
  - `todolist.models.Task` : core model with fields `task` (char) and `completed` (boolean).
  - Django views expose both server-rendered pages and lightweight JSON API endpoints used by the React UI (no DRF used).
  - URLs are defined in `todolist/urls.py` and mounted at the project root in `todo_manager/urls.py`.

- Frontend: React (CDN) + Tailwind (Play CDN)
  - `todolist/templates/todolist.html` mounts a React app that talks to the JSON endpoints for list/create/update/delete.
  - For quick prototyping we load React and Babel from CDN (development mode). For production you should build a proper React app.

Design & UX improvements made

- Animated, gentle header and consistent navbar across pages.
- Hero SVG and feature cards on the Home page for a professional look.
- React UI uses icons, animations, and Tailwind utilities for responsive styling.
- Server-rendered fallback list added so tasks are still visible if React fails.

React 19 note

- You asked for React 19. Currently this code uses React 18 via CDN for stability. When React 19 stable is available you can upgrade by:
  1. Replacing the CDN URLs with the React 19 equivalents (or installing `react@19` in your frontend build).
  2. Rebuilding the frontend bundle (if using a built frontend) and serving the static assets.

Production recommendations

- Move React into a proper frontend pipeline (create-react-app / Vite / Next) and build static assets.
- Integrate Tailwind via PostCSS/CLI and purge unused classes for smaller CSS.
- Protect destructive actions with POST-only endpoints and CSRF; consider permission checks.
- Add tests for API endpoints and views.

Run locally

```bash
# backend
python -m venv todo_env
# activate your venv (Windows example)
# todo_env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Notes

- This repo uses CDN-driven React and Tailwind for fast prototyping. For production, follow the "Production recommendations" section.
