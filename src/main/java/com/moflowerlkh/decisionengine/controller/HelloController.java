package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.service.HelloService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    @Autowired
    HelloService helloService;

    @GetMapping("/hello")
    public Long hello() {
        helloService.hello("");
        return System.currentTimeMillis();
    }
}