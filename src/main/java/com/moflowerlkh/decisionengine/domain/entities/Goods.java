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
@Table(name = "goods")
public class Goods extends BasePO {
    @Column(nullable = false)
    private Timestamp startTime;

    /**
     * 每人限购额度
     */
    @Column(name = "one_max_amount", nullable = false)
    private long oneMaxAmount;

    /**
     * 商品库存
     */
    @Column(name = "goods_amount", nullable = false)
    private long goodsAmount;

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
