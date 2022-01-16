package com.moflowerlkh.decisionengine.dao;

import com.moflowerlkh.decisionengine.entity.Ruler;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RulerDao extends JpaRepository<Ruler, Long> {
}
