from fastapi import FastAPI

from aegis.aegis import Aegis
from aegis.backends.redis_backend import RedisBackend
from aegis.middleware.rate_limit import RateLimitMiddleware

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
