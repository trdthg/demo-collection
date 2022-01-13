package com.moflowerlkh.decisionengine.model;

import lombok.Data;

import javax.persistence.*;
import java.sql.Timestamp;

@Entity
@Data
@Table(name = "shopping_activity_tb")
public class ShoppingActivity {
    @Id
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(nullable = false)
    private String info;

    // 统一使用 2022-01-01 20:00:00 时间格式
    @Column(nullable = false)
    private Timestamp beginTime;

    @Column(nullable = false)
    private Timestamp endTime;

    /**
     * 一个秒杀活动只能对应一个商品
     * 一个商品可能有多个秒杀活动
     */
    @JoinColumn(nullable = false)
    @ManyToOne
    private ShoppingGoods shoppingGoods;

    // 活动销售总数，不能超卖
    @Column(nullable = false)
    private long shoppingTotal;

    // 对应的规则
    @JoinColumn(nullable = false)
    @OneToOne
    private Ruler ruler;
}
