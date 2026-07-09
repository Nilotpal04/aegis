import time

from aegis.algorithms.base import RateLimiterAlgorithm
from aegis.core.token_bucket_state import TokenBucketState
from aegis.storage.base import Storage

class TokenBucket(RateLimiterAlgorithm):
    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        storage: Storage[TokenBucketState]
    ):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.storage = storage
        
    def allow(self, key: str) -> bool:
            current_time = time.time()
            
            state = self.storage.get(key)
            
            if state is None:
                state = TokenBucketState(
                    tokens=float(self.capacity),
                    last_refill=current_time,
                )
    
            elapsed = current_time - state.last_refill
            state.tokens = min(
                self.capacity,
                state.tokens + elapsed * self.refill_rate,
            )
    
            state.last_refill = current_time
            allowed = False

            if state.tokens >= 1:
                state.tokens -= 1
                allowed = True

            self.storage.set(key, state)
            return allowed