        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        
        local count =  redis.call("INCR", key)
        
        if count == 1 then
            redis.call("EXPIRE", key, window)
        end
        
        if count > limit then
            redis.call("DECR", key)
            return 0
        end
        
        return 1