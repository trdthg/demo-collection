package com.moflowerlkh.decisionengine.component;

import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.stereotype.Component;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.List;

@Component
@Log4j2
public class IpInterceptor implements HandlerInterceptor {

    @Autowired
    DefaultRedisScript<Boolean> defaultRedisScript;
    @Autowired
    StringRedisTemplate stringRedisTemplate;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        try {
            if (handler instanceof HandlerMethod) {
                HandlerMethod handlerMethod = (HandlerMethod) handler;
                AccessLimiter accessLimiter = handlerMethod.getMethodAnnotation(AccessLimiter.class);

                //判断是否有注解
                if (accessLimiter == null) {
                    return true;
                }
                String key = accessLimiter.key();
                Integer limit = accessLimiter.limit();
                Integer timeout = accessLimiter.timeout();

                // 1: 定义key是的列表
                List<String> keysList = new ArrayList<>();
                String ip = request.getRemoteAddr();
                keysList.add("IP_LIMIT" + "." + key + "." + ip);
                // 2:执行执行lua脚本限流
                String script =  defaultRedisScript.getScriptAsString();
                Boolean accessFlag = stringRedisTemplate.execute(defaultRedisScript, keysList, timeout.toString(), limit.toString());
                // 3: 判断当前执行的结果，如果是0，被限制，1代表正常
                if (Boolean.FALSE.equals(accessFlag)) {
                    log.warn("ip请求频繁");
                    response.setStatus(HttpServletResponse.SC_FORBIDDEN);
                    return false;
                }
                log.warn("ip请求成功");
                return true;
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
