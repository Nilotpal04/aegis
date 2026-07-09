from dataclasses import asdict, fields
from typing import Generic, TypeVar

from redis import Redis

from aegis.storage.base import Storage

State = TypeVar("State")


class RedisStorage(Storage[State], Generic[State]):
    def __init__(self, client: Redis, state_type: type[State]):
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

            raw_value = data.get(field_name)

            if raw_value is not None:
                if field_type is int:
                    converted[field_name] = int(raw_value)

                elif field_type is float:
                    converted[field_name] = float(raw_value)

                else:
                    converted[field_name] = raw_value

        return self.state_type(**converted)
