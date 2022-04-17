package com.moflowerlkh.decisionengine.component;

import javax.annotation.PostConstruct;

import lombok.extern.log4j.Log4j2;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

//import io.micrometer.core.instrument.Counter;
//import io.micrometer.core.instrument.MeterRegistry;

//@Aspect
//@Component
//@Log4j2
public class CountAspect {
    //@Autowired
    //MeterRegistry registry;
    //
    //private Counter counter;
    //
    //ThreadLocal<Long> startTime = new ThreadLocal<>();
    //
    //@Pointcut("execution(* com.moflowerlkh.decisionengine.controller.*.*(..))")
    //public void globalCount() {
    //}
    //
    //@PostConstruct
    //public void init() {
    //    this.counter = registry.counter("global_requests_count", "v1", "all");
    //}
    //
    //@Before("globalCount()")
    //public void doBefore(JoinPoint joinPoint) throws Throwable {
    //    startTime.set(System.currentTimeMillis());
    //    counter.increment();
    //}
    //
    //@Around("globalCount()")
    //public Object around(ProceedingJoinPoint point) throws Throwable {
    //    String methodName = point.getSignature().toShortString();
    //
    //    Object[] params = point.getArgs();
    //
    //    log.debug("{} start, request={}", methodName, params);
    //
    //    Object result;
    //    try {
    //        result = point.proceed();
    //    } catch (Exception e) {
    //        log.error("{} error, exception={}", methodName, e);
    //        throw e;
    //    }
    //
    //    if (log.isDebugEnabled()) {
    //        log.debug("{} end, result={}", methodName, result);
    //    }
    //    return result;
    //
    //}
    //
    //@AfterReturning(returning = "returnVal", pointcut = "globalCount()")
    //public void doAftereReturning(Object returnVal) {
    //    System.out.println("请求执行时间：" + (System.currentTimeMillis() - startTime.get()));
    //}

}
