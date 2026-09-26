# PolarTwin

PolarTwin is a responsive demonstration interface for exploring simulated operations at two fictional Antarctic research stations, Maitri and Bharati. It is a prototype and is not connected to NCPOR, MoES, real stations, sensors, satellites or emergency services. Do not use its sample readings or recommendations for operational decisions.

## Project layout

```text
.
├── backend/                 # FastAPI API and MongoDB integration
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/                # Vite + React application
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
├── .env                     # Local secrets; ignored by Git
├── .gitignore
├── docker-compose.yml        # Optional local MongoDB
└── README.md
```

## Frontend: local development

Requires Node.js 20.19+ or 22.12+.

```sh
cd frontend
npm ci
npm run dev
```

Open the Vite URL printed in the terminal. By default, the frontend expects the API at `http://127.0.0.1:8000`. To point it to another API, set `VITE_API_BASE_URL` before building or running Vite.

Build the static frontend with:

```sh
npm run build
```

The generated files are placed in `frontend/dist/`.

## Backend: local development

Requires Python 3.10+.

From the repository root, create and activate a virtual environment, then install the API requirements:

```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
```

Set the backend environment variables in your shell or hosting dashboard:

| Variable | Purpose | Local default |
|---|---|---|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGODB_DATABASE` | Database name | `polartwin_demo` |
| `POLARTWIN_AUTH_SECRET` | HMAC signing key for account tokens | Temporary random value if omitted |
| `POLARTWIN_CORS_ORIGINS` | Comma-separated allowed frontend origins | `http://localhost:5173,http://127.0.0.1:5173` |

The application reads environment variables directly; it does not load `.env` automatically. For local PowerShell development, configure them in the shell before starting the API. Never commit `.env` or put secrets in frontend variables.

Start the API from the repository root:

```sh
uvicorn backend.app.main:app --reload
```

Interactive API docs are at `http://127.0.0.1:8000/docs`; health status is at `http://127.0.0.1:8000/api/health`. The WebSocket endpoint is `ws://127.0.0.1:8000/ws/telemetry`.

### Optional local MongoDB with Docker

From the repository root:

```sh
docker compose up -d mongodb
```

The compose file stores MongoDB data in a named Docker volume. Stop it with `docker compose down`. `docker compose down -v` removes the volume and its data.

## Deployment

Deploy the frontend and backend as separate services, and use MongoDB Atlas for the database.

### Backend on Render

Connect this repository as a Render Web Service and configure:

- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Set these environment variables in Render (do not commit values to Git):

- `MONGODB_URI` — MongoDB Atlas URI with a rotated database password.
- `MONGODB_DATABASE` — `polartwin_demo`.
- `POLARTWIN_AUTH_SECRET` — long, random secret; keep it stable between deploys.
- `POLARTWIN_CORS_ORIGINS` — exact deployed frontend origin, such as `https://your-project.vercel.app`.

Add the Render service's network access in MongoDB Atlas as required by your cluster's network policy. After deployment, check `https://<render-service>.onrender.com/api/health`; MongoDB should report `ok`.

### Frontend on Vercel

Import the repository as a Vercel project and configure:

- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Environment Variable:** `VITE_API_BASE_URL` set to the Render service origin, such as `https://your-api.onrender.com`.

After Vercel deploys, copy its exact site origin into Render's `POLARTWIN_CORS_ORIGINS` and redeploy the backend if needed. The frontend sends login and registration requests to the backend. Other dashboard views primarily use local simulated demo data.

## Prototype capabilities and limitations

The frontend uses React, Vite, Recharts, Framer Motion and Lucide. The FastAPI service exposes demonstration endpoints for station status, environment, energy, equipment, inventory, alerts, analytics, predictions, accounts and simulated WebSocket telemetry. MongoDB stores demo station records, telemetry and registered accounts. Passwords use scrypt hashes; account tokens are HMAC-signed and expire after seven days.

This prototype does not implement real sensor ingestion, operational integrations, role authorization, email verification, password reset, rate limiting or production identity controls. Validate and secure it before using it beyond a demonstration.
