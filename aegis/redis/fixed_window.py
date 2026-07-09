from redis import Redis

from aegis.redis.base import RedisLuaAlgorithm
class RedisFixedWindow(RedisLuaAlgorithm):
    def __init__(
        self,
        limit: int,
        window_size: int,
        client: Redis
    ):
        super().__init__(
            client=client,
            lua_file="fixed_window.lua"
        )
        
        self.limit = limit
        self.window_size = window_size
        
    def allow(self, key: str) -> bool:
        result = self._execute(
            key,
            self.limit,
            self.window_size
        )
        
        return bool(result)