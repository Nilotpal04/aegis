import time
from app.algorithms.base import RateLimiterAlgorithm
from app.core.state import WindowState
from app.storage.base import Storage

class FixedWindow(RateLimiterAlgorithm):
    def __init__(self, limit: int, window_size: int, storage: Storage[WindowState]):
        self.limit = limit
        self.window_size = window_size
        self.storage = storage
        
    def allow(self, key: str) -> bool:
        
        current_time = time.time()
        state = self.storage.get(key)
        
        if state is None:
            self.storage.set(key, WindowState(count=1, window_start=current_time))
            return True
        
        window_expired = current_time - state.window_start >= self.window_size
        if window_expired:
            self.storage.set(key, WindowState(count=1, window_start=current_time))
            return True
        
        if state.count >= self.limit:
            return False
        
        state.count += 1
        self.storage.set(key, state)
        return True