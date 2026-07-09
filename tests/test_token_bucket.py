import time

from aegis.algorithms.token_bucket import TokenBucket
from aegis.core.token_bucket_state import TokenBucketState
from aegis.storage.memory import InMemoryStorage


def test_first_request_is_allowed():
    storage = InMemoryStorage[TokenBucketState]()
    limiter = TokenBucket(
        capacity=3,
        refill_rate=1,
        storage=storage,
    )

    result = limiter.allow("user123")

    assert result is True
    state = storage.get("user123")
    assert state is not None
    assert state.tokens == 2


def test_bucket_capacity_is_enforced():
    storage = InMemoryStorage[TokenBucketState]()
    limiter = TokenBucket(
        capacity=3,
        refill_rate=1,
        storage=storage,
    )

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False


def test_tokens_refill_after_time():
    storage = InMemoryStorage[TokenBucketState]()
    limiter = TokenBucket(
        capacity=2,
        refill_rate=1,
        storage=storage,
    )

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False

    time.sleep(1.1)
    assert limiter.allow("user123") is True


def test_users_are_rate_limited_independently():
    storage = InMemoryStorage[TokenBucketState]()
    limiter = TokenBucket(
        capacity=2,
        refill_rate=1,
        storage=storage,
    )

    assert limiter.allow("Neel") is True
    assert limiter.allow("Neel") is True
    assert limiter.allow("Neel") is False

    assert limiter.allow("Luna") is True
    assert limiter.allow("Luna") is True
    assert limiter.allow("Luna") is False
