package com.moflowerlkh.decisionengine.dao;

import com.moflowerlkh.decisionengine.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserDao extends JpaRepository<User, Long> {
}
