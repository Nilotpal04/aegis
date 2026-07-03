from pathlib import Path
from redis import Redis

class RedisLeakyBucket:
    def __init__(
        self,
        capacity: int,
        leak_rate: float,
        client: Redis,
    ):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.client = client

        lua_path = (Path(__file__).parent.parent/ "lua"/ "leaky_bucket.lua")

        with open(lua_path, "r") as f:
            self.lua_script = f.read()

        self.lua_script_sha = self.client.script_load(
            self.lua_script
        )

    def allow(self, key: str) -> bool:
        result = self.client.evalsha(
            self.lua_script_sha,
            1,
            key,
            self.capacity,
            self.leak_rate,
        )

        return bool(result)