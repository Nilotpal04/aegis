local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])

local now = redis.call("TIME")
local current = tonumber(now[1]) + tonumber(now[2]) / 1000000

local tokens = redis.call("HGET", key, "tokens")
local last_refill = redis.call("HGET", key, "last_refill")

if tokens == false or tokens == nil then
    redis.call(
        "HSET",
        key,
        "tokens",
        capacity - 1,
        "last_refill",
        current
    )

    redis.call(
        "EXPIRE",
        key,
        math.ceil(capacity / refill_rate) + 1
    )

    return 1
end

tokens = tonumber(tokens)
last_refill = tonumber(last_refill)

local elapsed = current - last_refill
local new_tokens = elapsed * refill_rate

tokens = math.min(
    capacity,
    tokens + new_tokens
)

last_refill = current

local allowed = 0

if tokens >= 1 then
    tokens = tokens - 1
    allowed = 1
end

redis.call(
    "HSET",
    key,
    "tokens",
    tokens,
    "last_refill",
    last_refill
)

redis.call(
    "EXPIRE",
    key,
    math.ceil(capacity / refill_rate) + 1
)

return allowed