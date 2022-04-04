package com.moflowerlkh.decisionengine.util;

import org.apache.logging.log4j.util.Strings;
import org.springframework.util.DigestUtils;

import java.nio.charset.StandardCharsets;
import java.util.List;

public class MD5 {
    public static String md5(List<String> args) {
        String arg = Strings.join(args, '.');
        return DigestUtils.md5DigestAsHex(arg.getBytes(StandardCharsets.UTF_8));
    }
}
