import time

from app.algorithms.base import RateLimiterAlgorithm
from app.core.state import WindowState

class FixedWindow(RateLimiterAlgorithm):
    def __init__(self, limit: int, window_size: int):
        
        self.limit = limit
        self.window_size = window_size
        self.windows: dict[str, WindowState] = {}
        
    def allow(self, key: str) -> bool:
        
        current_time = time.time()
        state = self.windows.get(key)
        
        if state is None:
            self.windows[key] = WindowState(count=1, window_start=current_time)
            return True
        
        if current_time - state.window_start >= self.window_size:
            self.windows[key] = WindowState(count=1, window_start=current_time)
            return True
        
        if state.count >= self.limit:
            return False
        
        state.count += 1
        return True