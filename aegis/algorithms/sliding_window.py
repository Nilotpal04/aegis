import time
from collections import deque

from aegis.algorithms.base import RateLimiterAlgorithm
from aegis.core.sliding_window_state import SlidingWindowState
from aegis.storage.base import Storage

class SlidingWindow(RateLimiterAlgorithm):
    def __init__(
        self,
        limit: int,
        window_size: int,
        storage: Storage[SlidingWindowState]
    ):
        self.limit = limit
        self.window_size = window_size
        self.storage = storage
        
    def allow(self, key: str) -> bool:
        current_time = time.time()
        state = self.storage.get(key)

        if state is None:
            state = SlidingWindowState(requests=deque())

        timestamps = state.requests
        cutoff = current_time - self.window_size

        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

        if len(timestamps) >= self.limit:
            return False

        timestamps.append(current_time)
        self.storage.set(key, state)
        return True