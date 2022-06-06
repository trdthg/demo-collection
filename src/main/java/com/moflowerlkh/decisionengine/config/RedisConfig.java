package com.moflowerlkh.decisionengine.config;

import com.alibaba.fastjson.support.spring.GenericFastJsonRedisSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<Object, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<Object, Object> template = new RedisTemplate<>();
        // 配置连接工厂
        template.setConnectionFactory(redisConnectionFactory);
        // 配置 key 的序列化方式
        template.setKeySerializer(new StringRedisSerializer());
        // 使用 Jackson2JsonRedisSerializer 配置 value 的序列化方式
        //template.setValueSerializer(new Jackson2JsonRedisSerializer<>(Object.class));
        // 使用 FastJson 配置 value 的序列化方式
        template.setValueSerializer(new GenericFastJsonRedisSerializer());
        return template;
    }
}
