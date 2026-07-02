from typing import Generic, TypeVar
from app.storage.base import Storage

State = TypeVar("State")
class InMemoryStorage(Storage[State], Generic[State]):
    """In-memory storage implementation for rate limiting."""
    
    def __init__(self):
        """Initialize an empty in-memory storage."""
        self.windows: dict[str, State] = {}
    
    def get(self, key: str) -> State | None:
        """Retrieve the WindowState for a given key"""
        return self.windows.get(key)
    
    def set(self, key: str, state: State) -> None:
        """Store a WindowState for a given key"""
        self.windows[key] = state