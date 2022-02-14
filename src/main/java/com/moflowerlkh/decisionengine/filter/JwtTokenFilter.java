package com.moflowerlkh.decisionengine.filter;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.util.JwtUtil;
import com.moflowerlkh.decisionengine.util.RedisUtil;
import com.moflowerlkh.decisionengine.vo.LoginUser;
import io.jsonwebtoken.lang.Strings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@Component
public class JwtTokenFilter extends OncePerRequestFilter {

    @Autowired
    RedisUtil redisUtil;

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
        System.out.println(token);
        if (!JwtUtil.validate(token)) {
            throw new RuntimeException("token已经过期");
        }
        // 解析
        try {
            String userID = JwtUtil.getUserIDFromToken(token);
            System.out.println("1: " + userID);
            System.out.println(userID);
            Object o = redisUtil.get("pc_token_" + userID);
            System.out.println("2: " + o);
            LoginUser loginUser = (LoginUser) o;
            System.out.println("3: " + loginUser);
            UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(loginUser, null, null);
            SecurityContextHolder.getContext().setAuthentication(authentication);
        } catch (Exception e) {
            throw new RuntimeException("token不合法");
        }
        // 放行
        chain.doFilter(request, response);
    }
}
