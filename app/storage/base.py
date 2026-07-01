from abc import ABC, abstractmethod
from app.core.state import WindowState
from typing import Optional

class Storage(ABC):
    
    @abstractmethod
    def get(self, key: str) -> Optional[WindowState]:
        """Get (count, window_start) for a give key"""
        pass
    
    @abstractmethod
    def set(self, key: str, state: WindowState) -> None:
        """Store the state associated with a client key."""
        pass