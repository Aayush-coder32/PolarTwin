# PolarTwin

**A Digital Twin for Smarter Antarctic Operations.** A responsive mission control prototype for the fictional operational monitoring of Maitri and Bharati stations.

> **Demonstration only.** All telemetry, station conditions, alerts, predictions and locations displayed in this prototype are illustrative simulated data. The prototype has no connection to NCPOR, MoES, Antarctic station systems, emergency services, satellites or physical IoT devices. It must not be used to make operational decisions.

## Run the frontend

Requires Node.js 20.19+ or 22.12+.

```sh
npm install
npm run dev
```

Open the Vite URL in a browser. Choose **Explore the digital twin** to create an account or **Sign in** to use an existing account. Account records are stored in MongoDB; passwords are hashed with scrypt and the API issues expiring signed bearer tokens.

## Run the demonstration API

Start MongoDB locally (Docker):

```sh
docker compose up -d mongodb
```

Or use an existing MongoDB instance. Configure `MONGODB_URI` and optionally `MONGODB_DATABASE` in the environment. The local `.env` file can hold these values; keep it private and never commit it. Defaults are `mongodb://localhost:27017` and `polartwin_demo`.

Python 3.10+:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

For local development, the API generates a temporary signing secret automatically. Set `POLARTWIN_AUTH_SECRET` to a persistent random value before starting the API if sessions must remain valid across API restarts; production deployments must provide and securely manage this secret.

API documentation is available at `http://127.0.0.1:8000/docs`. WebSocket telemetry is at `ws://127.0.0.1:8000/ws/telemetry`. The WebSocket emits clearly labeled simulated readings every four seconds. Set `POLARTWIN_CORS_ORIGINS` to a comma-separated allowlist when serving the API from another local origin.

The API creates MongoDB collections and indexes for stations, equipment, inventory, alerts, telemetry and maintenance tickets, and seeds the fictional station/system records on startup. The `/api/health` endpoint reports whether MongoDB is reachable. Stop local MongoDB with `docker compose down`; persistent demo data remains in its named Docker volume. Use `docker compose down -v` only if you intend to remove that volume and its demo records.

## Demonstration flow

1. Open mission control and switch between Maitri and Bharati from the station selector.
2. Explore the interactive site schematic and click infrastructure zones.
3. Use **Trigger demo anomaly** in equipment or alerts to create a simulated high-priority alert.
4. Review predictive maintenance and logistics forecasts.
5. Acknowledge an alert, compare both stations, open the emergency operations view, and ask PolarAI about the demo data.
6. Download a daily station summary. The export explicitly marks its contents as demonstration data.

## Prototype scope

The frontend uses React, Vite, Recharts, Framer Motion and Lucide icons. A Python FastAPI service supplies typed demonstration endpoints for stations, health, environment, energy, equipment, inventory, alerts, analytics and predictions, plus a WebSocket simulator. The interface intentionally labels telemetry and AI recommendations as simulated. Emergency mode is only an in-app demonstration view.

Redis, MQTT ingestion, actual sensor provisioning and trained AI models are **not implemented** by this prototype. Account registration and login use MongoDB-backed accounts, scrypt password hashes and expiring HMAC-signed bearer tokens. This prototype auth is not a substitute for production identity controls; production deployment also requires role authorization, email verification, password reset, audit logging, rate limiting, secret management, operational validation and formal security review.
