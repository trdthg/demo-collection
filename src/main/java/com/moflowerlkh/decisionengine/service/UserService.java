package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    UserDao userDao;

    public void register(User user) throws Exception {
        userDao.save(user);
    }

}

class PartialUser {
    Long id;
    String name;
}