from pathlib import Path

from redis import Redis
from redis.exceptions import NoScriptError


class RedisLuaAlgorithm:
    def __init__(self, client: Redis, lua_file: str):
        self.client = client
        self.lua_file = lua_file
        self._load_script()

    def _load_script(self):
        lua_path = Path(__file__).parent.parent / "lua" / self.lua_file

        with open(lua_path) as f:
            self.lua_script = f.read()

        self.script_sha = self.client.script_load(self.lua_script)

    def _execute(self, key: str, *args):
        try:
            return self.client.evalsha(self.script_sha, 1, key, *args)
        except NoScriptError:
            self._load_script()

            return self.client.evalsha(self.script_sha, 1, key, *args)
