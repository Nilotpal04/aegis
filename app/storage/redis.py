from dataclasses import asdict, fields
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
        
    def set(self, key: str, state: State) -> None:
        data = asdict(state)
        
        self.client.hset(key, mapping=data)
        
    def get(self, key: str) -> State | None:
        data = self.client.hgetall(key)
        
        if not data:
            return None
        
        converted = {}
        for field in fields(self.state_type):
            field_name = field.name
            field_type = field.type
            
            raw_value = data.get(field_name.encode('utf-8'))
            if raw_value is not None:
                value_str = raw_value.decode('utf-8')
                if field_type == int:
                    converted[field_name] = int(value_str)
                elif field_type == float:
                    converted[field_name] = float(value_str)
                else:
                    converted[field_name] = value_str
                    
        return self.state_type(**converted)
                    