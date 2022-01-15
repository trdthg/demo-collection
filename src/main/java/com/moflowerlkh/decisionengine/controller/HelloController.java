package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.service.HelloService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    @Autowired
    HelloService helloSevice;

    @GetMapping("/hello")
    public String hello(String arg) {
        System.out.println(arg);
        return "hello" + "ssss";
    }
}