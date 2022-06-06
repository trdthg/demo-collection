package com.moflowerlkh.decisionengine.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.scripting.support.ResourceScriptSource;

@Configuration
public class LuaConfig {
    /**
     * 将 lua 脚本的内容加载出来放入到 DefaultRedisScript
     */
    @Bean
    public DefaultRedisScript<Boolean> limitUserAccessLua() {
        // 1：初始化一个 lua 脚本的对象 DefaultRedisScript
        DefaultRedisScript<Boolean> defaultRedisScript = new DefaultRedisScript<>();
        // 2: 通过这个对象去加载 lua 脚本的位置 ClassPathResource 读取类路径下的 lua 脚本
        // ClassPathResource 什么是类路径：就是你 maven 编译好的 target/classes 目录
        defaultRedisScript.setScriptSource(new ResourceScriptSource(new ClassPathResource("userlimit.lua")));
        // 3: lua 脚本最终的返回值是什么？建议大家都是数字返回。1/0
        defaultRedisScript.setResultType(Boolean.class);
        return defaultRedisScript;
    }
}