from redis import Redis

class RedisBackend:
    def __init__(
        self, 
        host: str = "localhost",
        port: int = 6379,
        decode_responses: bool = True
    ):
        self.client = Redis(
            host=host,
            port=port,
            decode_responses=decode_responses
        )