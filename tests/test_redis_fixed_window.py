from redis import Redis
from aegis.redis.fixed_window  import RedisFixedWindow
import time

client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def test_first_request_is_allowed():
    client.flushdb()
    
    limiter = RedisFixedWindow(
        limit=3,
        window_size=60,
        client=client
    )
    
    result = limiter.allow("user123")
    
    assert result is True
    assert client.get("user123") == "1"
    
def test_limiter_is_enforced():
    client.flushdb()
    
    limiter = RedisFixedWindow(
        limit=3,
        window_size=60,
        client=client
    )
    
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
    assert client.get("user123") == "3"

def test_expire_is_set():
    client.flushdb()
    
    limiter = RedisFixedWindow(
        limit=3,
        window_size=60,
        client=client
    )
    
    limiter.allow("user123")
    
    ttl = client.ttl("user123")
    assert ttl > 0 
    assert ttl <= 60  
    
def test_window_expires():
    client.flushdb()
    
    window_size = 1
    limiter = RedisFixedWindow(
        limit=3,
        window_size=window_size,
        client=client
    )
    
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
    time.sleep(window_size + 0.1) 
    
    assert limiter.allow("user123") is True