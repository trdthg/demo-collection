package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.dao.RulerDao;
import com.moflowerlkh.decisionengine.dao.ShoppingActivityDao;
import com.moflowerlkh.decisionengine.entity.Ruler;
import com.moflowerlkh.decisionengine.entity.ShoppingActivity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HelloService {
    @Autowired
    RulerDao rulerDao;

    @Autowired
    ShoppingActivityDao shoppingActivityDao;

    public void hello(String arg) {
//        List<Ruler> rulers = rulerDao.findAll();
//        List<ShoppingActivity> i = shoppingActivityDao.findAll();
//        i.get(0).getRuler();
//        System.out.println("hello");
    }
}
