package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.GoodsOrder;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface GoodsOrderDao extends JpaRepository<GoodsOrder, Long> {
    List<GoodsOrder> findByGoodsID(Long goodsId);
}
