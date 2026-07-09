from redis import Redis

from aegis.redis.base import RedisLuaAlgorithm


class RedisLeakyBucket(RedisLuaAlgorithm):
    def __init__(
        self,
        capacity: int,
        leak_rate: float,
        client: Redis,
    ):
        super().__init__(client=client, lua_file="leaky_bucket.lua")

        self.capacity = capacity
        self.leak_rate = leak_rate

    def allow(self, key: str) -> bool:
        result = self._execute(key, self.capacity, self.leak_rate)

        return bool(result)
