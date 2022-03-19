package com.moflowerlkh.decisionengine.component;

import io.micrometer.core.annotation.Timed;
import io.micrometer.core.aop.TimedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class Aspect {
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }

}

