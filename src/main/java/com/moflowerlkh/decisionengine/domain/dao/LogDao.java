package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.Log;

import org.springframework.data.jpa.repository.JpaRepository;

public interface LogDao extends JpaRepository<Log, Long> {
}
