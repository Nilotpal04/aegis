import time

from redis import Redis

from aegis.redis.leaky_bucket import RedisLeakyBucket

client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


def test_first_request_is_allowed():
    client.flushdb()

    limiter = RedisLeakyBucket(
        capacity=3,
        leak_rate=1.0,
        client=client,
    )

    assert limiter.allow("user123") is True

    assert float(client.hget("user123", "water")) == 1.0
    assert client.hget("user123", "last_leak") is not None


def test_capacity_is_enforced():
    client.flushdb()

    limiter = RedisLeakyBucket(
        capacity=3,
        leak_rate=0.0,
        client=client,
    )

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False

    remaining = float(client.hget("user123", "water"))
    assert remaining >= 2.0


def test_water_leaks_over_time():
    client.flushdb()

    limiter = RedisLeakyBucket(
        capacity=1,
        leak_rate=1.0,
        client=client,
    )

    assert limiter.allow("user123") is True
    assert limiter.allow("user123") is False

    time.sleep(1.1)

    assert limiter.allow("user123") is True


def test_users_are_rate_limited_independently():
    client.flushdb()

    limiter = RedisLeakyBucket(
        capacity=2,
        leak_rate=0.0,
        client=client,
    )

    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is True
    assert limiter.allow("user1") is False

    assert limiter.allow("user2") is True
    assert limiter.allow("user2") is True
    assert limiter.allow("user2") is False


def test_bucket_sets_ttl():
    client.flushdb()

    limiter = RedisLeakyBucket(
        capacity=5,
        leak_rate=1.0,
        client=client,
    )

    limiter.allow("user123")

    ttl = client.ttl("user123")

    assert ttl > 0
