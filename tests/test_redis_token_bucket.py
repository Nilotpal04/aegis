import time

from redis import Redis

from aegis.redis.token_bucket import RedisTokenBucket

client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


def test_first_request_is_allowed():
    client.flushdb()

    limiter = RedisTokenBucket(
        capacity=3,
        refill_rate=1.0,
        client=client,
    )

    result = limiter.allow("user123")

    assert result is True
    assert float(client.hget("user123", "tokens")) == 2.0
    assert client.hget("user123", "last_refill") is not None


def test_bucket_capacity_is_enforced():
    client.flushdb()

    limiter = RedisTokenBucket(
        capacity=3,
        refill_rate=1.0,
        client=client,
    )

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False

    remaining = float(client.hget("user123", "tokens"))
    assert 0.0 <= remaining < 1.0


def test_tokens_refill_after_time():
    client.flushdb()

    limiter = RedisTokenBucket(
        capacity=3,
        refill_rate=1.0,
        client=client,
    )

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False

    time.sleep(1.1)

    assert limiter.allow("user123") is True

    remaining = float(client.hget("user123", "tokens"))
    assert 0.0 <= remaining < 1.0


def test_users_are_rate_limited_independently():
    client.flushdb()

    limiter = RedisTokenBucket(
        capacity=2,
        refill_rate=1.0,
        client=client,
    )

    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is False

    assert limiter.allow("user2") is True
    assert limiter.allow("user2") is True
    assert limiter.allow("user2") is False

    remaining = float(client.hget("user1", "tokens"))
    assert 0.0 <= remaining < 1.0

    remaining = float(client.hget("user2", "tokens"))
    assert 0.0 <= remaining < 1.00


def test_bucket_sets_ttl():
    client.flushdb()

    limiter = RedisTokenBucket(
        capacity=5,
        refill_rate=1.0,
        client=client,
    )

    limiter.allow("user123")

    ttl = client.ttl("user123")

    assert ttl > 0
