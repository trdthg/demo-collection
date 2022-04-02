package com.moflowerlkh.decisionengine.util;

import io.jsonwebtoken.CompressionCodecs;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.stereotype.Component;

import java.util.Date;

/**
 * @Description: TokenManager
 */
@Component
public class JwtUtil {
    private static final long tokenExpiration = 1000 * 60 * 60 * 6;
    private static final long refreshTokenExpiration = 1000 * 60 * 60 * 24 * 7;
    private static final String tokenSignKey = "123456";
    // private static final String userRoleKey = "userRole";

    // 就是id，只是函数签名之前忘了改
    public static String createToken(String userId) {
        return Jwts.builder()
                .setSubject(userId)
                .setExpiration(new Date(System.currentTimeMillis() + tokenExpiration))
                .signWith(SignatureAlgorithm.HS512, tokenSignKey).compressWith(CompressionCodecs.GZIP).compact();
    }

    public static String createRefreshToken(String userId) {
        return Jwts.builder()
                .setSubject(userId)
                .setExpiration(new Date(System.currentTimeMillis() + refreshTokenExpiration))
                .signWith(SignatureAlgorithm.HS512, tokenSignKey).compressWith(CompressionCodecs.GZIP).compact();
    }

    public static String getUserIDFromToken(String token) {
        return Jwts.parser().setSigningKey(tokenSignKey).parseClaimsJws(token).getBody().getSubject();
    }

    public static boolean validate(String token) {
        try {
            Jwts.parser().setSigningKey(tokenSignKey).parse(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}