import time

from aegis.algorithms.base import RateLimiterAlgorithm
from aegis.core.leaky_bucket_state import LeakyBucketState
from aegis.storage.base import Storage

class LeakyBucket(RateLimiterAlgorithm):
    def __init__(
        self,
        capacity: int,
        leak_rate: float,
        storage: Storage[LeakyBucketState]
    ):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.storage = storage
        
    def allow(self, key: str) -> bool:
        current_time = time.time()
        state = self.storage.get(key)
        
        if state is None:
            state = LeakyBucketState(water=0.0, last_leak=current_time)
            
        elapsed = current_time - state.last_leak
        state.water = max(0, state.water - elapsed * self.leak_rate)
        
        state.last_leak = current_time
        
        allowed = False
        
        if state.water < self.capacity:
            state.water += 1
            allowed = True
        
        self.storage.set(key, state)
        return allowed