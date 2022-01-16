package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.RulerDao;
import com.moflowerlkh.decisionengine.dao.ShoppingActivityDao;
import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.Ruler;
import com.moflowerlkh.decisionengine.entity.ShoppingActivity;
import com.moflowerlkh.decisionengine.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HelloService {
    @Autowired
    RulerDao rulerDao;

    @Autowired
    ShoppingActivityDao shoppingActivityDao;

    @Autowired
    UserDao userDao;

    public void hello(String arg) {
        List<User> users = userDao.findAll();
        System.out.println(users);
        if (users.isEmpty()) {
            User newUser = new User();
            newUser.setId(112L);
            newUser.setUsername("asd");
            newUser.setPassword("asd");
            newUser.setYearIncome(10L);
            newUser.setGender("男");
            newUser.setAge(18);
            userDao.save(newUser);
        } else {
            users.get(0).setAge(users.get(0).getAge() + 1);
            userDao.saveAndFlush(users.get(0));
        }
//        List<Ruler> rulers = rulerDao.findAll();
//        List<ShoppingActivity> i = shoppingActivityDao.findAll();
//        i.get(0).getRuler();
//        System.out.println("hello");
    }
}
