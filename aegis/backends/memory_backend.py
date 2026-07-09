from aegis.storage.memory import InMemoryStorage

from aegis.algorithms.fixed_window import FixedWindow
from aegis.algorithms.sliding_window import SlidingWindow
from aegis.algorithms.token_bucket import TokenBucket
from aegis.algorithms.leaky_bucket import LeakyBucket

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