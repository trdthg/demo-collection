package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.enums.Gender;
import com.moflowerlkh.decisionengine.util.JwtUtil;
import com.moflowerlkh.decisionengine.util.RedisUtil;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.service.LoginUser;
import io.swagger.annotations.*;
import lombok.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.*;

@RestController
@Api(value = "authController", tags = {"登陆授权相关"})
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    AuthenticationManager authenticationManager;
    @Autowired
    RedisUtil redisUtil;

    @PostMapping("/signin")
    @ResponseBody
    @ApiOperation(value = "登陆", notes = "token 6小时过期，refreshToken 7天过期")
    //@ApiResponses(value={
    //    @ApiResponse(code=200, message="OK", response = JwtResponse.class),
    //    @ApiResponse(code = 403, message = "用户名和密码错误", response = String.class),
    //    @ApiResponse(code = 500, message = "未知错误，请联系管理员", response = String.class),
    //})
    public BaseResponse<JwtResponse> authenticateUser(@RequestBody LoginRequest loginRequest) {
        Authentication authentication;
        try {
            authentication = authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword()));
        } catch (UsernameNotFoundException e) {
            return new BaseResponse<>(HttpStatus.FORBIDDEN, "没有该用户");
        } catch (BadCredentialsException e) {
            return new BaseResponse<>(HttpStatus.FORBIDDEN, "密码错误");
        } catch (Exception e) {
            return new BaseResponse<>(HttpStatus.INTERNAL_SERVER_ERROR, "未知错误，请联系管理员");
        }
        if (authentication == null) {
            return new BaseResponse<>(HttpStatus.FORBIDDEN, "认证失败");
        }
        // 获取用户认证信息
        LoginUser loginUser = (LoginUser) authentication.getPrincipal();
        User user = loginUser.getUser();
        String token = JwtUtil.createToken(user.getId().toString());
        String refreshToken = JwtUtil.createRefreshToken(user.getId().toString());
        val jwtResponse = new JwtResponse(token, refreshToken, user.getId(), user.getUsername(), user.getGender());
        // 把token存入redis
        redisUtil.set("pc_token_" + user.getId(), loginUser);
        return new BaseResponse<>(jwtResponse);
    }

    @GetMapping("/logout")
    @ResponseBody
    @ApiOperation(value = "登出", notes = "登陆状态(需要token)下🥬使用")
    public BaseResponse<String> logout() {
        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder.getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        Long userid = loginUser.getUser().getId();
        redisUtil.del("pc_token_" + userid);
        return new BaseResponse<>("登出成功");
    }

    @GetMapping("/hello")
    @ResponseBody
    @ApiOperation(value = "hello", notes = "不需要登陆")
    public BaseResponse<String> aaaa() {
        return new BaseResponse<>("hello: aa");
    }

    @GetMapping("/hello2")
    @PreAuthorize("hasAuthority('test')")
    @ResponseBody
    @ApiOperation(value = "hello2", notes = "登陆状态(需要token)下🥬使用 + 需要的角色: ['test']")
    public BaseResponse<String> aaaab() {
        return new BaseResponse<>("hello");
    }


    @GetMapping("/hello3")
    @PreAuthorize("hasAuthority('fuck')")
    @ResponseBody
    @ApiOperation(value = "hello3", notes = "登陆状态(需要token)下🥬使用 + 需要的角色: ['fuck']")
    public BaseResponse<String> aaaabc() {
        return new BaseResponse<>("hello");
    }

    @PostMapping("/refreshtoken")
    @ResponseBody
    @ApiOperation(value = "刷新token", notes = "使用refreshToken交换refreshToken")
    public BaseResponse<TokenRefreshResponse> refreshtoken(@RequestBody RefreshRequest request) {
        String refreshToken = request.getRefreshToken();
        if (JwtUtil.validate(refreshToken)) {
            String userID = JwtUtil.getUserIDFromToken(refreshToken);
            String token = JwtUtil.createToken(userID);
            TokenRefreshResponse response = new TokenRefreshResponse(token, refreshToken);
            return new BaseResponse<>(response);
        }
        return new BaseResponse<>(HttpStatus.UNAUTHORIZED, "refresh token 已经过期，请重新登录");
    }
}

@Data
@NoArgsConstructor
@AllArgsConstructor
class LoginRequest {
    private String username;
    private String password;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
class RefreshRequest {
    private String refreshToken;
}

@Data
@AllArgsConstructor
class JwtResponse {
    private String token;
    private String refreshToken;
    private Long id;
    private String username;
    private Gender gender;
}

@Data
@AllArgsConstructor
class TokenRefreshResponse {
    private String token;
    private String refreshToken;
}