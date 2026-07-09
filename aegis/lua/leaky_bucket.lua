local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local leak_rate = tonumber(ARGV[2])

local now = redis.call("TIME")
local current = tonumber(now[1]) + tonumber(now[2]) / 1000000

local water = redis.call("HGET", key, "water")
local last_leak = redis.call("HGET", key, "last_leak")

if water == false or water == nil then
    water = 0
    last_leak = current
else
    water = tonumber(water)
    last_leak = tonumber(last_leak)
end

local elapsed = current - last_leak

water = math.max(
    0,
    water - elapsed * leak_rate
)

last_leak = current

local allowed = 0

if water + 1 <= capacity then
    water = water + 1
    allowed = 1
end

redis.call(
    "HSET",
    key,
    "water",
    water,
    "last_leak",
    last_leak
)

if leak_rate > 0 then
    local ttl = math.ceil(capacity / leak_rate) + 1
    redis.call("EXPIRE", key, ttl)
end

return allowed