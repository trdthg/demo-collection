package com.moflowerlkh.decisionengine.domain.entities;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import java.util.Objects;

/**
 * 秒杀商品
 */
@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Table(name = "shopping_goods_tb")
public class ShoppingGoods extends BasePO {

    @Column(nullable = false)
    private String name;

    @Column(nullable = true)
    private String info;

    // 商品总数
    @Column(nullable = false)
    private Long goodsAmount;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        ShoppingGoods that = (ShoppingGoods) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
