from dataclasses import asdict
from typing import Generic, TypeVar

from redis import Redis
from app.storage.base import Storage

State = TypeVar("State")

class RedisStorage(Storage[State], Generic[State]):
    def __init__(
        self,
        client: Redis,
        state_type: type[State]
    ):
        self.client = client
        self.state_type = state_type
        
    def set(self, key: str, state = State) -> None:
        data = asdict(state)
        
        self.client.hset(key, mapping=data)
        
    def get(self, key: str) -> State | None:
        date = self.client.hgetall(key)