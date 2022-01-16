package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.User;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

public class UserService {

    @Autowired
    UserDao userDao;

    @Autowired


    public List<User> getAllUser() {
        return userDao.findAll();
    }

    public List<User> getAllPassedUser(long activityID) {

        return null;
    }

}
