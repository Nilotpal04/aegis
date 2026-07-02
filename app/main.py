from fastapi import FastAPI

from app.algorithms.fixed_window import FixedWindow
from app.middleware.rate_limit import RateLimitMiddleware
from app.storage.memory import InMemoryStorage
from app.core.sliding_window_state import SlidingWindowState
from app.algorithms.sliding_window import SlidingWindow

storage = InMemoryStorage[SlidingWindowState]()

limiter = SlidingWindow(
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
