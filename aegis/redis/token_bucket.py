from redis import Redis

from aegis.redis.base import RedisLuaAlgorithm


class RedisTokenBucket(RedisLuaAlgorithm):
    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        client: Redis,
    ):
        super().__init__(client=client, lua_file="token_bucket.lua")

        self.capacity = capacity
        self.refill_rate = refill_rate

    def allow(self, key: str) -> bool:
        result = self._execute(key, self.capacity, self.refill_rate)

        return bool(result)
