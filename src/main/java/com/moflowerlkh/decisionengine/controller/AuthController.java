package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.component.AccessLimiter;
import com.moflowerlkh.decisionengine.component.RequestLimiter;
import com.moflowerlkh.decisionengine.service.AuthService;
import com.moflowerlkh.decisionengine.service.AuthServiceDTO.JwtResponse;
import com.moflowerlkh.decisionengine.service.AuthServiceDTO.LoginRequest;
import com.moflowerlkh.decisionengine.service.AuthServiceDTO.RefreshRequest;
import com.moflowerlkh.decisionengine.service.AuthServiceDTO.TokenRefreshResponse;
import com.moflowerlkh.decisionengine.vo.BaseResponse;

//import io.micrometer.core.annotation.Timed;
import io.swagger.annotations.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.concurrent.TimeUnit;

@RestController
@Api(value = "authController", tags = { "登陆授权相关" })
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    AuthService authService;

    // @Timed("登陆")
    @PostMapping("/signin")
    @ResponseBody
    @ApiOperation(value = "登陆", notes = "token 6 小时过期，refreshToken 7 天过期")
    public BaseResponse<JwtResponse> authenticateUser(@RequestBody LoginRequest loginRequest) {
        return authService.signin(loginRequest);
    }

    @GetMapping("/logout")
    @ResponseBody
    @ApiOperation(value = "登出", notes = "登陆状态 (需要 token) 下🥬使用")
    public BaseResponse<String> logout() {
        return authService.logout();
    }

    @PostMapping("/refreshtoken")
    @ResponseBody
    @ApiOperation(value = "刷新 token", notes = "使用 refreshToken 交换 refreshToken")
    public BaseResponse<TokenRefreshResponse> refreshtoken(@RequestBody RefreshRequest request) {
        return authService.refrehToken(request);
    }

    @AccessLimiter(key = "hello", limit = 10, timeout = 2)
    @RequestLimiter(QPS = 300, timeout = 1)
    // @Timed(value = "auth.hello", description = "Time taken to request hello1
    // endpoint")
    @GetMapping("/hello")
    @ResponseBody
    @ApiOperation(value = "hello", notes = "不需要登陆")
    public BaseResponse<String> hello() {
        return new BaseResponse<>("hello: aa");
    }

    // @Timed(value = "auth.hello2", description = "Time taken to request hello1
    // endpoint")
    @GetMapping("/hello2")
    @PreAuthorize("hasAuthority('test')")
    @ResponseBody
    @ApiOperation(value = "hello2", notes = "登陆状态 (需要 token) 下🥬使用 + 需要的角色: ['test']")
    public BaseResponse<String> hello2() {
        return new BaseResponse<>("hello");
    }

    @GetMapping("/hello3")
    @PreAuthorize("hasAuthority('fuck')")
    @ResponseBody
    @ApiOperation(value = "hello3", notes = "登陆状态 (需要 token) 下🥬使用 + 需要的角色: ['fuck']")
    public BaseResponse<String> hello3() {
        return new BaseResponse<>("hello");
    }

}
