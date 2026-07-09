from redis import Redis

from app.redis.fixed_window import RedisFixedWindow
from app.redis.sliding_window import RedisSlidingWindow
from app.redis.token_bucket import RedisTokenBucket
from app.redis.leaky_bucket import RedisLeakyBucket

REDIS_LIMITERS = {
    "fixed_window": RedisFixedWindow,
    "sliding_window": RedisSlidingWindow,
    "token_bucket": RedisTokenBucket,
    "leaky_bucket": RedisLeakyBucket,
}
class RedisBackend:
    def __init__(
        self, 
        host: str = "localhost",
        port: int = 6379,
        decode_responses: bool = True
    ):
        self.client = Redis(
            host=host,
            port=port,
            decode_responses=decode_responses
        )
    
    def create_limiter(
        self,
        algorithm: str,
        **kwargs,
    ):
        limiter_class = REDIS_LIMITERS.get(algorithm)
        
        if limiter_class is None:
            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            )
        
        return limiter_class(
            client=self.client,
            **kwargs
        )