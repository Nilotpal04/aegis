from app.storage.memory import InMemoryStorage

from app.algorithms.fixed_window import FixedWindow
from app.algorithms.sliding_window import SlidingWindow
from app.algorithms.token_bucket import TokenBucket
from app.algorithms.leaky_bucket import LeakyBucket

MEMORY_LIMITERS = {
    "fixed_window": FixedWindow,
    "sliding_window": SlidingWindow,
    "token_bucket": TokenBucket,
    "leaky_bucket": LeakyBucket,
}
class MemoryBackend:
    def __init__(self):
        self.storage = InMemoryStorage()
    
    def create_limiter(
        self,
        algorithm: str,
        **kwargs,
    ):
        limiter_class = MEMORY_LIMITERS.get(algorithm)
        
        if limiter_class is None:
            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            )
        
        return limiter_class(
            storage=self.storage,
            **kwargs
        )