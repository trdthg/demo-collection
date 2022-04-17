package com.moflowerlkh.decisionengine.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.scripting.support.ResourceScriptSource;

@Configuration
public class LuaConfig {
    /**
     * 将lua脚本的内容加载出来放入到DefaultRedisScript
     */
    @Bean
    public DefaultRedisScript<Boolean> limitUserAccessLua() {
        // 1： 初始化一个lua脚本的对象DefaultRedisScript
        DefaultRedisScript<Boolean> defaultRedisScript = new DefaultRedisScript<>();
        // 2: 通过这个对象去加载lua脚本的位置 ClassPathResource读取类路径下的lua脚本
        // ClassPathResource 什么是类路径：就是你maven编译好的target/classes目录
        defaultRedisScript.setScriptSource(new ResourceScriptSource(new ClassPathResource("userlimit.lua")));
        // 3: lua脚本最终的返回值是什么？建议大家都是数字返回。1/0
        defaultRedisScript.setResultType(Boolean.class);
        return defaultRedisScript;
    }
}