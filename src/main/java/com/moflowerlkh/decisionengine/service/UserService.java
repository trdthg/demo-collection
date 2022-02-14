package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    UserDao userDao;

    public ResponseEntity<?> register(User user) {
        System.out.println("用户输入的：" + user);
        try {
            user.setId(12L);
            User u = userDao.save(user);
            System.out.println("注册成功");
            return new ResponseEntity<>(user, HttpStatus.OK);
        } catch (Exception e) {
            System.out.println("注册失败");
            return new ResponseEntity<>("注册失败", HttpStatus.BAD_REQUEST);
        }
    }

    public ResponseEntity<?> login(String username, String password) {
        return ResponseEntity.ok("");
    }

}
