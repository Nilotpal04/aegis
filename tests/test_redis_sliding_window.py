import time
from redis import Redis
from aegis.redis.sliding_window import RedisSlidingWindow

client = Redis(host="localhost", port=6379, decode_responses=True)

def test_first_request_is_allowed():
    client.flushdb()
    
    limiter = RedisSlidingWindow(limit=3, window_size=10, client=client)
    
    result = limiter.allow("user123")
    
    assert result is True
    assert client.zcard("user123") == 1


def test_limit_is_enforced():
    client.flushdb()
    
    limiter = RedisSlidingWindow(limit=3, window_size=10, client=client)
    
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
    assert client.zcard("user123") == 3


def test_expired_entries_are_removed():
    client.flushdb()
    
    window_size = 1 
    limiter = RedisSlidingWindow(limit=3, window_size=window_size, client=client)
    
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
    time.sleep(window_size + 0.1)
    
    assert limiter.allow("user123") is True
    assert client.zcard("user123") == 1 


def test_users_are_rate_limited_independently():
    client.flushdb()
    
    limiter = RedisSlidingWindow(limit=2, window_size=10, client=client)
    
    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is False
    
    assert limiter.allow("user2") is True
    assert limiter.allow("user2") is True
    assert limiter.allow("user2") is False
    
    assert client.zcard("user1") == 2
    assert client.zcard("user2") == 2