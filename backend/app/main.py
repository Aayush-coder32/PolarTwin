"""PolarTwin demonstration API.

Returns clearly labeled fictional demonstration data; it is not connected to
Maitri, Bharati, NCPOR, station devices, emergency services or a live database.
"""
from __future__ import annotations

import asyncio
import os
import random
import hashlib
import hmac
import secrets
import time
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError
from pydantic import BaseModel, Field

DEMO = True
STATIONS: dict[str, dict[str, Any]] = {
    "maitri": {"id": "maitri", "name": "Maitri", "location": "Queen Maud Land", "latitude": "70°45′S", "longitude": "11°44′E", "temperature_c": -18.4, "wind_kmh": 28, "battery_pct": 84, "health_pct": 94, "load_pct": 72, "generation_kw": 418, "personnel": 47, "fuel_pct": 68},
    "bharati": {"id": "bharati", "name": "Bharati", "location": "Larsemann Hills", "latitude": "69°24′S", "longitude": "76°11′E", "temperature_c": -21.2, "wind_kmh": 34, "battery_pct": 79, "health_pct": 91, "load_pct": 67, "generation_kw": 386, "personnel": 35, "fuel_pct": 76},
}
EQUIPMENT = [
    {"id": "g-02", "name": "Generator G-02", "health_pct": 82, "vibration_mm_s": 7.8, "temperature_c": 76.2, "risk": "MEDIUM"},
    {"id": "h-01", "name": "HVAC Unit H-01", "health_pct": 96, "vibration_mm_s": 2.1, "temperature_c": 42.1, "risk": "LOW"},
    {"id": "b-03", "name": "Battery Bank B-03", "health_pct": 91, "vibration_mm_s": 0.3, "temperature_c": -12.4, "risk": "LOW"},
]
INVENTORY = [
    {"name": "Diesel fuel", "remaining_pct": 68, "estimated_days": 42, "status": "OPTIMAL"},
    {"name": "Food provisions", "remaining_pct": 82, "estimated_days": 61, "status": "OPTIMAL"},
    {"name": "Medical supplies", "remaining_pct": 91, "estimated_days": 96, "status": "OPTIMAL"},
    {"name": "Spare parts", "remaining_pct": 54, "estimated_days": 35, "status": "WATCH"},
    {"name": "Emergency batteries", "remaining_pct": 38, "estimated_days": 24, "status": "WATCH"},
]
ALERTS = [
    {"id": "demo-g02-vibration", "station": "Maitri", "severity": "HIGH", "category": "EQUIPMENT", "description": "Generator G-02 vibration is above its simulated baseline.", "action": "Inspect during the next safe maintenance window.", "is_demo": True},
    {"id": "demo-wind-maitri", "station": "Maitri", "severity": "MEDIUM", "category": "ENVIRONMENT", "description": "Elevated simulated winds; review outdoor activity plans.", "action": "Review field work and secure exposed equipment.", "is_demo": True},
]

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "polartwin_demo")
AUTH_SECRET = os.getenv("POLARTWIN_AUTH_SECRET") or secrets.token_hex(32)
mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2500)
db = mongo_client[MONGODB_DATABASE]
stations_collection = db["stations"]
equipment_collection = db["equipment"]
inventory_collection = db["inventory"]
alerts_collection = db["alerts"]
telemetry_collection = db["telemetry"]
maintenance_collection = db["maintenance"]
users_collection = db["users"]

app = FastAPI(title="PolarTwin Demonstration API", version="1.0.0", description="Fictional Antarctic station data for the PolarTwin prototype. Not connected to operational station systems.")
origins = [origin.strip() for origin in os.getenv("POLARTWIN_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])


@app.middleware("http")
async def require_account_session(request, call_next):
    public_paths = {"/api/health", "/api/auth/register", "/api/auth/login"}
    if request.url.path.startswith("/api/") and request.url.path not in public_paths:
        try:
            current_user(request.headers.get("authorization"))
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return await call_next(request)


class AcknowledgeBody(BaseModel):
    acknowledged_by: str = Field(min_length=2, max_length=120)


class MaintenanceBody(BaseModel):
    station_id: str = Field(min_length=1, max_length=32)
    equipment_id: str = Field(min_length=1, max_length=32)
    description: str = Field(min_length=4, max_length=500)
    scheduled_for: str | None = None


class AuthBody(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=10, max_length=128)
    name: str = Field(min_length=2, max_length=80)


class LoginBody(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=1, max_length=128)


def password_hash(password: str, salt: bytes | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex(), digest.hex()


def issue_token(user_id: str) -> str:
    payload = f"{user_id}:{int(time.time()) + 60 * 60 * 24 * 7}"
    signature = hmac.new(AUTH_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{signature}"


def current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer ") or not AUTH_SECRET:
        raise HTTPException(status_code=401, detail="Please sign in to continue")
    try:
        user_id, expires, signature = authorization[7:].rsplit(":", 2)
        payload = f"{user_id}:{expires}"
        expected = hmac.new(AUTH_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if int(expires) < int(time.time()) or not hmac.compare_digest(signature, expected):
            raise ValueError("invalid token")
        user = users_collection.find_one({"id": user_id}, {"_id": 0, "password_salt": 0, "password_hash": 0})
        if not user:
            raise ValueError("unknown user")
        return user
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Could not reach the account database") from exc
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Session expired. Please sign in again.") from exc


def station_or_404(station_id: str) -> dict[str, Any]:
    try:
        result = stations_collection.find_one({"id": station_id.lower()}, {"_id": 0})
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="MongoDB is unavailable. Start MongoDB and retry.") from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return result


def mongo_ready() -> bool:
    try:
        mongo_client.admin.command("ping")
        return True
    except PyMongoError:
        return False


@app.on_event("startup")
def initialize_mongodb():
    if not mongo_ready():
        # Let the web/API process start so health reports the actionable dependency state.
        return
    stations_collection.create_index([("id", ASCENDING)], unique=True)
    equipment_collection.create_index([("id", ASCENDING)], unique=True)
    inventory_collection.create_index([("name", ASCENDING)], unique=True)
    alerts_collection.create_index([("id", ASCENDING)], unique=True)
    telemetry_collection.create_index([("station_id", ASCENDING), ("timestamp_utc", ASCENDING)])
    maintenance_collection.create_index([("ticket_id", ASCENDING)], unique=True)
    users_collection.create_index([("email", ASCENDING)], unique=True)
    for station in STATIONS.values():
        stations_collection.update_one({"id": station["id"]}, {"$setOnInsert": station}, upsert=True)
    for asset in EQUIPMENT:
        equipment_collection.update_one({"id": asset["id"]}, {"$setOnInsert": asset}, upsert=True)
    for item in INVENTORY:
        inventory_collection.update_one({"name": item["name"]}, {"$setOnInsert": item}, upsert=True)
    for alert in ALERTS:
        alerts_collection.update_one({"id": alert["id"]}, {"$setOnInsert": {**alert, "acknowledged": False, "created_at_utc": datetime.now(timezone.utc).isoformat()}}, upsert=True)


@app.get("/api/health")
def health():
    connected = mongo_ready()
    return {"status": "ok" if connected else "degraded", "database": "mongodb" if connected else "unavailable", "demo": DEMO, "telemetry_source": "SIMULATED", "server_time_utc": datetime.now(timezone.utc).isoformat()}


@app.post("/api/auth/register")
def register(body: AuthBody):
    if not AUTH_SECRET:
        raise HTTPException(status_code=503, detail="Account service is not configured. Set POLARTWIN_AUTH_SECRET and restart the API.")
    try:
        email = body.email.strip().lower()
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise HTTPException(status_code=422, detail="Enter a valid email address")
        salt, hashed = password_hash(body.password)
        user = {"id": secrets.token_urlsafe(16), "email": email, "name": body.name.strip(), "password_salt": salt, "password_hash": hashed, "created_at_utc": datetime.now(timezone.utc).isoformat()}
        users_collection.insert_one(user)
        return {"token": issue_token(user["id"]), "user": {"id": user["id"], "email": email, "name": user["name"]}}
    except PyMongoError as exc:
        if getattr(exc, "code", None) == 11000:
            raise HTTPException(status_code=409, detail="An account with this email already exists") from exc
        raise HTTPException(status_code=503, detail="Could not save account. Check MongoDB and retry.") from exc


@app.post("/api/auth/login")
def authenticate(body: LoginBody):
    if not AUTH_SECRET:
        raise HTTPException(status_code=503, detail="Account service is not configured. Set POLARTWIN_AUTH_SECRET and restart the API.")
    try:
        user = users_collection.find_one({"email": body.email.strip().lower()})
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Could not reach the account database") from exc
    if not user:
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    salt = bytes.fromhex(user["password_salt"])
    _, hashed = password_hash(body.password, salt)
    if not hmac.compare_digest(hashed, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    return {"token": issue_token(user["id"]), "user": {"id": user["id"], "email": user["email"], "name": user["name"]}}


@app.get("/api/auth/me")
def auth_me(user: dict[str, Any] = Depends(current_user)):
    return {"user": user}


@app.get("/api/stations")
def stations():
    try:
        return {"demo": DEMO, "items": list(stations_collection.find({}, {"_id": 0}))}
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="MongoDB is unavailable. Start MongoDB and retry.") from exc


@app.get("/api/stations/{station_id}")
def station(station_id: str):
    return {"demo": DEMO, "station": station_or_404(station_id)}


@app.get("/api/stations/{station_id}/health")
def health_score(station_id: str):
    value = station_or_404(station_id)
    return {"demo": DEMO, "station_id": value["id"], "score_pct": value["health_pct"], "components": {"infrastructure": 96, "energy": 91, "environment": 95, "logistics": 88, "communication": 97}}


@app.get("/api/stations/{station_id}/environment")
def environment(station_id: str):
    value = station_or_404(station_id)
    result = {"demo": DEMO, "station_id": value["id"], "risk": "WATCH" if value["wind_kmh"] >= 28 else "NORMAL", "temperature_c": value["temperature_c"], "wind_kmh": value["wind_kmh"], "wind_direction": "ENE", "pressure_hpa": 987.4, "humidity_pct": 68, "snowfall_cm_h": 1.4, "visibility_km": 12.4, "solar_radiation_w_m2": 182, "air_quality_aqi": 18, "timestamp_utc": datetime.now(timezone.utc).isoformat()}
    try:
        telemetry_collection.insert_one({"station_id": value["id"], "type": "environment", **result})
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Could not save environmental telemetry to MongoDB.") from exc
    return result


@app.get("/api/stations/{station_id}/energy")
def energy(station_id: str):
    value = station_or_404(station_id)
    return {"demo": DEMO, "station_id": value["id"], "generation_kw": value["generation_kw"], "consumption_kw": 354, "battery_pct": value["battery_pct"], "daily_consumption_mwh": 8.7, "peak_load_kw": 472, "efficiency_pct": 91.4, "generation_mix_pct": {"diesel": 62, "solar": 24, "battery": 14}, "consumption_mix_pct": {"residential": 31, "laboratory": 24, "heating": 21, "communications": 11, "water": 8, "other": 6}}


@app.get("/api/stations/{station_id}/equipment")
def equipment(station_id: str):
    value = station_or_404(station_id)
    return {"demo": DEMO, "station_id": value["id"], "items": list(equipment_collection.find({}, {"_id": 0}))}


@app.get("/api/stations/{station_id}/inventory")
def inventory(station_id: str):
    value = station_or_404(station_id)
    return {"demo": DEMO, "station_id": value["id"], "items": list(inventory_collection.find({}, {"_id": 0}))}


@app.get("/api/stations/{station_id}/alerts")
def alerts(station_id: str):
    value = station_or_404(station_id)
    items = list(alerts_collection.find({"station": value["name"], "acknowledged": {"$ne": True}}, {"_id": 0}))
    return {"demo": DEMO, "station_id": value["id"], "items": items}


@app.get("/api/stations/{station_id}/analytics")
def analytics(station_id: str):
    value = station_or_404(station_id)
    return {"demo": DEMO, "station_id": value["id"], "period": "24h", "energy": [{"hour": h, "generation_kw": g, "consumption_kw": c} for h, g, c in [("00", 410, 340), ("03", 375, 310), ("06", 350, 365), ("09", 470, 430), ("12", 510, 472), ("15", 488, 415), ("18", 435, 390), ("21", 418, 355)]]}


@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge(alert_id: str, body: AcknowledgeBody):
    now = datetime.now(timezone.utc).isoformat()
    result = alerts_collection.update_one({"id": alert_id}, {"$set": {"acknowledged": True, "acknowledged_by": body.acknowledged_by, "acknowledged_at_utc": now}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"demo": DEMO, "alert_id": alert_id, "acknowledged": True, "acknowledged_by": body.acknowledged_by, "acknowledged_at_utc": now}


@app.post("/api/maintenance")
def create_maintenance(body: MaintenanceBody):
    station_or_404(body.station_id)
    if equipment_collection.find_one({"id": body.equipment_id}) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    ticket = {"demo": DEMO, "created": True, "ticket_id": f"PT-DEMO-{random.randint(1000, 9999)}", **body.model_dump(), "created_at_utc": datetime.now(timezone.utc).isoformat()}
    maintenance_collection.insert_one(ticket)
    return ticket


@app.get("/api/predictions")
def predictions(station_id: str = "maitri"):
    value = station_or_404(station_id)
    return {"demo": DEMO, "station_id": value["id"], "items": [{"type": "maintenance", "asset": "Generator G-02", "risk": "MEDIUM", "recommendation": "Review vibration at next safe maintenance window.", "confidence": "DEMONSTRATION ONLY"}, {"type": "supply", "asset": "Emergency batteries", "days_to_threshold": 24, "recommendation": "Consider replenishment in next planning window.", "confidence": "DEMONSTRATION ONLY"}]}


@app.get("/api/reports")
def reports():
    return {"demo": DEMO, "available": [{"type": "daily_station_summary", "format": "text/csv", "stations": list(STATIONS)}]}


def simulated_snapshot() -> dict[str, Any]:
    snapshot = {}
    for station in stations_collection.find({}, {"_id": 0}):
        key = station["id"]
        snapshot[key] = {"temperature_c": round(station["temperature_c"] + random.uniform(-0.08, 0.08), 1), "wind_kmh": max(2, round(station["wind_kmh"] + random.uniform(-1, 1))), "battery_pct": max(5, min(100, station["battery_pct"] + random.choice([-1, 0, 0, 1])))}
    timestamp = datetime.now(timezone.utc).isoformat()
    for station_id, reading in snapshot.items():
        telemetry_collection.insert_one({"station_id": station_id, "type": "realtime_snapshot", "source": "SIMULATED", "demo": DEMO, "timestamp_utc": timestamp, **reading})
    return {"type": "telemetry", "demo": DEMO, "source": "SIMULATED", "timestamp_utc": timestamp, "stations": snapshot}


@app.websocket("/ws/telemetry")
async def telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(simulated_snapshot())
            await asyncio.sleep(4)
    except WebSocketDisconnect:
        return
