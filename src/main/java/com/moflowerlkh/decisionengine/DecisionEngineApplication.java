package com.moflowerlkh.decisionengine;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

@SpringBootApplication
@EnableScheduling
@EnableWebMvc
@EnableJpaAuditing
public class DecisionEngineApplication {

    public static void main(String[] args) {
        SpringApplication.run(DecisionEngineApplication.class, args);
    }

}
