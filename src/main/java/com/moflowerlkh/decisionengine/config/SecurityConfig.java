package com.moflowerlkh.decisionengine.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

/**
 * @Description 拦截白名单
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()// 对请求授权
            .antMatchers("/doc.html", "/**").permitAll() //允许所有人访问knife4j
            .anyRequest() // 任何请求
            .authenticated()// 需要身份认证
        ;
    }


}

