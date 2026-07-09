import time
from aegis.algorithms.fixed_window import FixedWindow
from aegis.storage.memory import InMemoryStorage

def test_first_request_is_allowed():
    storage = InMemoryStorage()
    limiter = FixedWindow(limit=3, window_size=60, storage=storage)
    key = "user123"
    
    result = limiter.allow(key)

    assert result is True
    state = storage.get(key)
    assert state is not None
    assert state.count == 1
    assert state.window_start is not None
    
def test_request_limit_is_enforced():

    storage = InMemoryStorage()
    limiter = FixedWindow(limit=3, window_size=60, storage=storage)

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
def tests_window_resets_after_expiration():
    
    storage = InMemoryStorage()
    limiter = FixedWindow(limit=2, window_size=1, storage=storage)
    
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
    time.sleep(1.1)
    
    assert limiter.allow("user123") is True
    
def test_users_are_rate_limited_independently():
    
    storage = InMemoryStorage()
    limiter = FixedWindow(limit=2, window_size=60, storage=storage)
    
    # User A reaches the limit
    assert limiter.allow("Neel") is True
    assert limiter.allow("Neel") is True
    assert limiter.allow("Neel") is False
    
    # User B should still be allowed
    assert limiter.allow("Luna") is True 