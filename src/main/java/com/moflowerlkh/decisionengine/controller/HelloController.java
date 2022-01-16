package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.service.HelloService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Api(tags = "Hello Controller  00000")
@RestController
public class HelloController {
    @Autowired
    HelloService helloService;

    @ApiOperation("Helloooooooooooo!")
    @GetMapping("/hello")
    public Long hello() {
        helloService.hello("");
        return System.currentTimeMillis();
    }
}