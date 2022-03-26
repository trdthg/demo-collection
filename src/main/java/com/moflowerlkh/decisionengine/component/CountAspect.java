package com.moflowerlkh.decisionengine.component;

import javax.annotation.PostConstruct;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;

// @Aspect
// @Component
public class CountAspect {
    @Autowired
    MeterRegistry registry;

    private Counter counter;

    ThreadLocal<Long> startTime = new ThreadLocal<>();

    @Pointcut("execution(* com.moflowerlkh.decisionengine.controller.*.*(..))")
    public void globalCount() {
    }

    @PostConstruct
    public void init() {
        this.counter = registry.counter("global_requests_count", "v1", "all");
    }

    @Before("pointCut()")
    public void doBefore(JoinPoint joinPoint) throws Throwable {
        startTime.set(System.currentTimeMillis());
        counter.increment();
    }

    @AfterReturning(returning = "returnVal", pointcut = "globalCount()")
    public void doAftereReturning(Object returnVal) {
        System.out.println("请求执行时间：" + (System.currentTimeMillis() - startTime.get()));
    }

}
