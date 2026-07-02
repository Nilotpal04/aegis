import time
from app.storage.memory import InMemoryStorage
from app.algorithms.leaky_bucket import LeakyBucket
from app.core.leaky_bucket_state import LeakyBucketState

def test_first_request_is_allowed():
    storage = InMemoryStorage[LeakyBucketState]()
    limiter = LeakyBucket(
        capacity=3,
        leak_rate=1.0,
        storage=storage
    )
    
    result = limiter.allow("user123")
    
    assert result is True
    state = storage.get("user123")
    assert state is not None
    assert state.water == 1.0
    
def test_capacity_is_enforced():
    storage = InMemoryStorage[LeakyBucketState]()
    limiter = LeakyBucket(
        capacity=3,
        leak_rate=0.0,
        storage=storage
    )
    
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False
    
def test_water_leaks_over_time():
    storage = InMemoryStorage[LeakyBucketState]()

    old_time = time.time() - 2

    storage.set(
        "user123",
        LeakyBucketState(
            water=3.0,
            last_leak=old_time,
        ),
    )

    limiter = LeakyBucket(
        capacity=3,
        leak_rate=1.0,
        storage=storage,
    )

    assert limiter.allow("user123") is True
    
def test_users_are_rate_limited_independently():
    storage = InMemoryStorage[LeakyBucketState]()
    limiter = LeakyBucket(
        capacity=2,
        leak_rate=0.0,
        storage=storage
    )
    
    assert limiter.allow("Neel") is True
    assert limiter.allow("Neel") is True
    assert limiter.allow("Neel") is False
    
    assert limiter.allow("Luna") is True
    assert limiter.allow("Luna") is True
    assert limiter.allow("Luna") is False