package com.moflowerlkh.decisionengine.domain.entities;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;

import java.sql.Timestamp;
import java.util.Objects;

/**
 * 秒杀商品
 */
@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Table(name = "commodity")
public class Commodity extends BasePO {
    /**
     * 商品名称
     */
    @Column(name = "name", nullable = false)
    private String name;

    /**
     * 商品信息
     */
    @Column(name = "info", nullable = true)
    private String info;

    /**
     * 商品单价
     */
    @Column(name = "price", nullable = false)
    private long price;

    /**
     * 商品库存
     */
    @Column(name = "amount", nullable = false)
    private long amount;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        Goods that = (Goods) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
