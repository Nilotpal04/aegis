from fastapi import FastAPI

from app.algorithms.fixed_window import FixedWindow
from app.middleware.rate_limit import RateLimitMiddleware
from app.storage.memory import InMemoryStorage

storage = InMemoryStorage()

limiter = FixedWindow(
    limit=5, 
    window_size=60, 
    storage=storage,
)

app = FastAPI()

app.add_middleware(
    RateLimitMiddleware,
    limiter=limiter
)

@app.get("/")
async def home():
    return {"message": "Welcome to Aegis!"}
