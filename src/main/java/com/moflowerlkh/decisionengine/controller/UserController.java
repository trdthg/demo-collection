package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.service.UserService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@Api(tags = {"用户相关"})
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody User user) {
        return userService.register(user);
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(String username, String password) {
        return userService.login(username, password);
    }

    @GetMapping("/hello")
    @ApiOperation("打印hello xxx")
    public String hello(String username) {
        return "Hello" + username;
    }
}