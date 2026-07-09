from app.backends.redis_backend import RedisBackend

from app.redis.fixed_window import RedisFixedWindow
from app.redis.sliding_window import RedisSlidingWindow
from app.redis.leaky_bucket import RedisLeakyBucket
from app.redis.token_bucket import RedisTokenBucket

REDIS_LIMITERS = {
    "fixed_window": RedisFixedWindow,
    "sliding_window": RedisSlidingWindow,
    "token_bucket": RedisTokenBucket,
    "leaky_bucket": RedisLeakyBucket,
}

class Aegis:
    def __init__(
        self,
        backend: RedisBackend,
        algorithm: str,
        **kwargs
    ):
            
        limiter_class = REDIS_LIMITERS.get(algorithm)
        
        if limiter_class is None:
            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            )
        
        self.limiter = limiter_class(
            client=backend.client,
            **kwargs
        )
        
    def allow(self, key: str) -> bool:
        return self.limiter.allow(key)