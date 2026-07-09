from fastapi import FastAPI

from app.aegis import Aegis
from app.backends.redis_backend import RedisBackend
from app.middleware.rate_limit import RateLimitMiddleware

backend = RedisBackend()

limiter = Aegis(
    backend=backend,
    algorithm="fixed_window",
    limit=5,
    window_size=60,
)

app = FastAPI()

app.add_middleware(
    RateLimitMiddleware,
    limiter=limiter
)

@app.get("/")
async def home():
    return {"message": "Welcome to Aegis!"}
