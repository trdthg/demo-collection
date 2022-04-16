package com.moflowerlkh.decisionengine.config.filter;

import com.moflowerlkh.decisionengine.service.AuthService;
import com.moflowerlkh.decisionengine.service.LoginUser;
import com.moflowerlkh.decisionengine.util.JwtUtil;
import com.moflowerlkh.decisionengine.service.RedisService;

import io.jsonwebtoken.lang.Strings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.CredentialsExpiredException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@Component
public class JwtTokenFilter extends OncePerRequestFilter {

    @Autowired
    RedisService redisService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response,
            FilterChain chain)
            throws ServletException, IOException {
        // 拿到token, 没有就走其他过滤器
        final String token = request.getHeader(HttpHeaders.AUTHORIZATION);
        if (!Strings.hasText(token)) {
            chain.doFilter(request, response);
            return;
        }
        // 校验
        System.out.println("token: " + token);
        if (!JwtUtil.validate(token)) {
            throw new CredentialsExpiredException("token已经过期");
        }
        // 解析
        try {
            String userID = JwtUtil.getUserIDFromToken(token);
            System.out.println("2: " + userID);
            Object o = redisService.get(AuthService.PC_TOKEN + "." + userID);
            LoginUser loginUser = (LoginUser) o;
            //System.out.println("3: " + loginUser);
            //System.out.println("4: " + loginUser.getAuthorities());
            UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(loginUser,
                    null, loginUser.getAuthorities());
            SecurityContextHolder.getContext().setAuthentication(authentication);
            System.out.println("5: " + "认证成功");
        } catch (Exception e) {
            throw new BadCredentialsException("token不合法");
        }
        // 放行
        chain.doFilter(request, response);
    }
}
