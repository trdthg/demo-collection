package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.User;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UserDao extends JpaRepository<User, Long> {

    User findByUsername(String username);

    List<User> findByName(String name);

}
