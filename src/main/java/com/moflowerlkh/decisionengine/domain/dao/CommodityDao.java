package com.moflowerlkh.decisionengine.domain.dao;

import com.moflowerlkh.decisionengine.domain.entities.Commodity;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CommodityDao extends JpaRepository<Commodity, Long> {
}
