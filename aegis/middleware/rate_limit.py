from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from aegis.algorithms.base import RateLimiterAlgorithm

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: RateLimiterAlgorithm):
        super().__init__(app)
        self.limiter = limiter
        
    async def dispatch(self, request: Request, call_next):
        key = request.client.host if request.client else "unknown"
        
        if not self.limiter.allow(key):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
            )
        
        response = await call_next(request)
        return response