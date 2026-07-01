from app.core.state import WindowState
from app.storage.base import Storage

class InMemoryStorage(Storage):
    """In-memory storage implementation for rate limiting."""
    
    def __init__(self):
        """Initialize an empty in-memory storage."""
        self.windows: dict[str, WindowState] = {}
    
    def get(self, key: str) -> WindowState | None:
        """Retrieve the WindowState for a given key"""
        return self.windows.get(key)
    
    def set(self, key: str, state: WindowState) -> None:
        """Store a WindowState for a given key"""
        self.windows[key] = state