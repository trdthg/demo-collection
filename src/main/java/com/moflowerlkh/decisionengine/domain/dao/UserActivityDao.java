package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.UserActivity;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UserActivityDao extends JpaRepository<UserActivity, Long> {
    List<UserActivity> findByUserId(Long user_id);

    List<UserActivity> findByActivityId(Long activity_id);

    List<UserActivity> findByUserIdAndActivityId(Long user_id, Long acctivity_id);
}
