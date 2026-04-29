from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bot.storage import JsonStorage
from bot.vin_service import VinService

app = FastAPI(title="Car Mini App API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
storage = JsonStorage()
vin = VinService()


class UserReq(BaseModel):
    user_id: int


class AddVinReq(UserReq):
    vin: str


class ServiceReq(UserReq):
    title: str
    mileage: int
    cost: float
    category: str


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/api/garage")
def garage(req: UserReq):
    p = storage.get_profile(req.user_id)
    return {"profile": p, "active": storage.get_active_car(req.user_id)}


@app.post("/api/car/add_by_vin")
async def add_by_vin(req: AddVinReq):
    data = await vin.decode(req.vin)
    ok, msg = storage.add_car(req.user_id, data)
    if not ok:
        raise HTTPException(400, msg)
    return {"car": data}


@app.post("/api/car/switch/{idx}")
def switch_car(idx: int, req: UserReq):
    if not storage.set_active_car(req.user_id, idx):
        raise HTTPException(400, "invalid index")
    return {"ok": True}


@app.post("/api/service/add")
def add_service(req: ServiceReq):
    storage.add_service_record(req.user_id, req.title, req.mileage, req.cost, req.category)
    return {"ok": True}


@app.post("/api/history")
def history(req: UserReq):
    return {"items": storage.service_history(req.user_id)}


@app.post("/api/reminders")
def reminders(req: UserReq):
    car = storage.get_active_car(req.user_id)
    if not car:
        return {"items": []}
    mileage = int(car.get("mileage", 0))
    return {
        "items": [
            {"title": "Замена масла", "due_mileage": mileage + 9000, "status": "soon"},
            {"title": "ГРМ", "due_mileage": mileage + 70000, "status": "actual"},
            {"title": "Тормоза", "due_mileage": mileage + 15000, "status": "actual"},
        ]
    }


@app.post("/api/stats")
def stats(req: UserReq):
    return storage.expense_stats(req.user_id)


@app.post('/api/admin')
def admin(req: UserReq):
    # Access should be validated by bot/admin ids at gateway layer
    return storage.analytics()
