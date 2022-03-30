package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.ShoppingGoods;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ShoppingGoodsDao extends JpaRepository<ShoppingGoods, Long> {
}
