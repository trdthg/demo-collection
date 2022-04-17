package com.moflowerlkh.decisionengine.component;

import com.google.common.util.concurrent.RateLimiter;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Component;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 请求限流拦截器
 *
 * @author xhq
 * @version 1.0
 * @date 2019/10/22 16:46
 */
@Component
@Log4j2
public class RequestLimiterInterceptor implements HandlerInterceptor {

    /**
     * 不同的方法存放不同的令牌桶
     */
    private final Map<String, RateLimiter> rateLimiterMap = new ConcurrentHashMap<>();

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        try {
            if (handler instanceof HandlerMethod) {
                HandlerMethod handlerMethod = (HandlerMethod) handler;
                RequestLimiter rateLimit = handlerMethod.getMethodAnnotation(RequestLimiter.class);
                //判断是否有注解
                if (rateLimit != null) {
                    // 获取请求url
                    String url = request.getRequestURI();
                    RateLimiter rateLimiter;
                    // 判断map集合中是否有创建好的令牌桶
                    if (!rateLimiterMap.containsKey(url)) {
                        // 创建令牌桶,以n r/s往桶中放入令牌
                        rateLimiter = RateLimiter.create(rateLimit.QPS());
                        rateLimiterMap.put(url, rateLimiter);
                    }
                    rateLimiter = rateLimiterMap.get(url);
                    // 获取令牌
                    boolean acquire = rateLimiter.tryAcquire(rateLimit.timeout(), rateLimit.timeunit());
                    if (acquire) {
                        //获取令牌成功
                        log.warn("请求成功,url:{}", request.getServletPath());
                        return true;
                    } else {
                        log.warn("请求被限流,url:{}", request.getServletPath());
                        response.setStatus(HttpServletResponse.SC_FORBIDDEN);
                        //response.write(response, new GenericResult(StateCode.ERROR_SERVER, rateLimit.msg()));
                        return false;
                    }
                }
            }
            return true;
        } catch (Exception var6) {
            var6.printStackTrace();
            //this.write(response, new GenericResult(StateCode.ERROR, "对不起,请求似乎出现了一些问题,请您稍后重试！"));
            return false;
        }
    }

}