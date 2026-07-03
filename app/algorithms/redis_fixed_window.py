from redis import Redis

class RedisFixedWindow:
    def __init__(
        self,
        limit: int,
        window_size: int,
        client: Redis
    ):
        self.limit = limit
        self.window_size = window_size
        self.client = client
        
    def allow(self, key: str) -> bool:
        count = self.client.incr(key)
        
        if count == 1:
            self.client.expire(key, self.window_size)
        
        if count > self.limit:
            return False
        
        return True