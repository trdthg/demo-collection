package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.dao.UserDao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class UserdetailsService {
    @Autowired
    UserDao userDao;

    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        System.out.println("username: " + username);
        User user = userDao.findByUsername(username);
        System.out.println("user: " + user);
        if (user == null) {
            throw new UsernameNotFoundException("没有该用户");
        }

        Set<String> permissions = new HashSet<>(Arrays.asList("test", "fucker"));
        user.setRoles(permissions);
        return new LoginUser(user);
    }
}
