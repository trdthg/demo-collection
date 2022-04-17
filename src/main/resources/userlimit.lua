-- 为某个接口的请求IP设置计数器，比如：127.0.0.1请求课程接口
-- KEYS[1] = 127.0.0.1 也就是用户的IP
-- ARGV[1] = 过期时间 30m
-- ARGV[2] = 限制的次数
local limitCount = redis.call('incr',KEYS[1]);
if limitCount == 1 then
  redis.call("expire",KEYS[1],ARGV[1])
end
-- 如果次数还没有过期，并且还在规定的次数内，说明还在请求同一接口
if limitCount > tonumber(ARGV[2]) then
  return 0
end
return 1