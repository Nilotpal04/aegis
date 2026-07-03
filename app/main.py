from fastapi import FastAPI

from app.algorithms.fixed_window import FixedWindow
from app.middleware.rate_limit import RateLimitMiddleware
from app.storage.memory import InMemoryStorage
from app.core.sliding_window_state import SlidingWindowState
from app.algorithms.sliding_window import SlidingWindow
from app.algorithms.redis_fixed_window import RedisFixedWindow
from redis import Redis

from app.storage.redis import RedisStorage
from app.core.state import WindowState

client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

storage = RedisStorage(
    client=client,
    state_type=WindowState,
)

limiter = RedisFixedWindow(
    limit=5, 
    window_size=60, 
    client=client,
)

app = FastAPI()

app.add_middleware(
    RateLimitMiddleware,
    limiter=limiter
)

@app.get("/")
async def home():
    return {"message": "Welcome to Aegis!"}
