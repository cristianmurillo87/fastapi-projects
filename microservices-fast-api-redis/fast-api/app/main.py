import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel, get_redis_connection

from .consumers import create_delivery, start_delivery

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "fastapi"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis",
    port="6379",
    password="testingredisforthefirsttime",
    decode_responses=True,
)


class Delivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = redis


@app.get("/deliveries/{pk}/status")
async def get_state(pk: str):
    state = redis.get(f"delivery:{pk}")
    return json.loads(state) if state is not None else {}


@app.post("/deliveries/create")
async def create(request: Request):
    body = await request.json()
    delivery = Delivery(
        budget=body["data"]["budget"], notes=body["data"]["notes"]
    ).save()
    event = Event(
        delivery_id=delivery.pk, type=body["type"], data=json.dumps(body["data"])
    ).save()
    state = create_delivery({}, event)
    redis.set(f"delivery:{delivery.pk}", json.dumps(state))
    return state


@app.post("/event")
async def dispatch(request: Request):
    body = await request.json()
    delivery_id = body.get("delivery_id")
    type = body.get("type")
    data = json.dumps(body.get("data", {}))
    event = Event(delivery_id=delivery_id, type=type, data=data).save()
    state = await get_state(delivery_id)
    new_state = start_delivery(state, event)
    redis.set(f"delivery:{delivery_id}", json.dumps(new_state))
    return new_state
