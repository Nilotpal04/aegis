from redis import Redis
from pathlib import Path
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
        
        lua_path = Path(__file__).parent.parent / "lua" / "fixed_window.lua"
        with open(lua_path, "r") as f:
            self.lua_script = f.read()
            
        self.lua_script_sha = self.client.script_load(self.lua_script)
        
    def allow(self, key: str) -> bool:
        result = self.client.evalsha(
            self.lua_script_sha,
            1,
            key,
            self.limit,
            self.window_size
        )
        
        return bool(result)