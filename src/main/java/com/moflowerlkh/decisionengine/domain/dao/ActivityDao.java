package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.Activity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;


public interface ActivityDao extends JpaRepository<Activity, Long> {
    Page<Activity> findAllByType(Pageable pageable, Integer type);
}

