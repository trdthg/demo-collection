package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.vo.LoginUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class UserdetailsService {
    @Autowired
    UserDao userDao;

    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userDao.findByUsername(username);
        System.out.println("1" + user);
        System.out.println("2" + user.getUsername());
        if (user.getAge() > 0) {
            throw new UsernameNotFoundException("没有该用户");
        }

        return new LoginUser(user);
    }
}
