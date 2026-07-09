from redis import Redis

from aegis.core.state import WindowState
from aegis.storage.redis import RedisStorage

client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

def test_set_and_get_window_state():
    client.flushdb()
    
    storage = RedisStorage(
        client=client,
        state_type=WindowState
    )
    
    state = WindowState(
        count=5,
        window_start=123.45,
    )
    
    storage.set("user123", state)
    loaded = storage.get("user123")
    
    assert loaded is not None
    assert loaded.count == 5
    assert loaded.window_start  == 123.45
    
def test_missing_key_returns_none():
    client.flushdb()
    
    storage = RedisStorage(
        client=client,
        state_type=WindowState
    )
    
    loaded = storage.get("does_not_exist")
    assert loaded is None
    
def test_type_preservation():
    client.flushdb()
    
    storage = RedisStorage(
        client=client,
        state_type=WindowState
    )
    
    state = WindowState(
        count=5,
        window_start=123.45
    )
    
    storage.set("user123", state)
    loaded = storage.get("user123")
    
    assert isinstance(loaded.count, int)
    assert isinstance(loaded.window_start, float)
    