local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local now = redis.call("TIME")

local current = tonumber(now[1]) + tonumber(now[2]) / 1000000

local cutoff = current - window

redis.call(
    "ZREMRANGEBYSCORE",
    key,
    "-inf",
    cutoff
)

local count = redis.call("ZCARD", key)

if count >= limit then
    return 0
end

redis.call(
    "ZADD",
    key,
    current,
    tostring(current)
)

    redis.call("EXPIRE", key, window)

return 1