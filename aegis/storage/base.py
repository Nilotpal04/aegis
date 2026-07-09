from abc import ABC, abstractmethod
from typing import Generic, TypeVar

State = TypeVar("State")

class Storage(ABC, Generic[State]):
    
    @abstractmethod
    def get(self, key: str) -> State | None:
        """Get (count, window_start) for a give key"""
        pass
    
    @abstractmethod
    def set(self, key: str, state: State) -> None:
        """Store the state associated with a client key."""
        pass