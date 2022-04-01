package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.Goods;

import org.springframework.data.jpa.repository.JpaRepository;

public interface GoodsDao extends JpaRepository<Goods, Long> {
}
