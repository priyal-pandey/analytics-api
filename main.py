
import os
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_a72ed8otbkdbgs76xkjufp73"
EMAIL = "23f2005558@ds.study.iitm.ac.in"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    body: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = body.events
    user_totals = defaultdict(float)

    revenue = 0.0

    for event in events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] += event.amount

    top_user = (
        max(user_totals, key=user_totals.get)
        if user_totals
        else ""
    )

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len({event.user for event in events}),
        "revenue": revenue,
        "top_user": top_user,
    }


@app.get("/")
def home():
    return {"status": "ok", "endpoint": "/analytics"}

