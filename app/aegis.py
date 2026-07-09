from app.backends.redis_backend import RedisBackend
from app.backends.memory_backend import MemoryBackend

from app.redis.fixed_window import RedisFixedWindow
from app.redis.sliding_window import RedisSlidingWindow
from app.redis.leaky_bucket import RedisLeakyBucket
from app.redis.token_bucket import RedisTokenBucket

from app.algorithms.fixed_window import FixedWindow
from app.algorithms.sliding_window import SlidingWindow
from app.algorithms.token_bucket import TokenBucket
from app.algorithms.leaky_bucket import LeakyBucket


REDIS_LIMITERS = {
    "fixed_window": RedisFixedWindow,
    "sliding_window": RedisSlidingWindow,
    "token_bucket": RedisTokenBucket,
    "leaky_bucket": RedisLeakyBucket,
}

MEMORY_LIMITERS = {
    "fixed_window": FixedWindow,
    "sliding_window": SlidingWindow,
    "token_bucket": TokenBucket,
    "leaky_bucket": LeakyBucket,
}


class Aegis:
    def __init__(
        self,
        backend,
        algorithm: str,
        **kwargs,
    ):
        if isinstance(backend, RedisBackend):
            registry = REDIS_LIMITERS
            
        elif isinstance(backend, MemoryBackend):
            registry = MEMORY_LIMITERS
            
        else:
            raise ValueError("Unsupported backend")
        
        limiter_class = registry.get(algorithm)
        
        if limiter_class is None:
            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            )
            
        if isinstance(backend, RedisBackend):
            self.limiter = limiter_class(
                client=backend.client,
                **kwargs,
            )
            
        else:
            self.limiter = limiter_class(
                storage=backend.storage,
                **kwargs,
            )
            
    def allow(self, key: str) -> bool:
        return self.limiter.allow(key)