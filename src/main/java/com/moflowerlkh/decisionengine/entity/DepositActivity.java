package com.moflowerlkh.decisionengine.entity;

import lombok.Data;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 *                        秒杀规则 1 - 1 秒杀活动 n - +
 *                                                  |
 * @Description 秒杀活动   秒杀规则 1 - 1 秒杀活动 n - 1 商品
 */
@Entity
@Data
@Table(name = "shopping_activity_tb")
public class DepositActivity {
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

    // 存款额度下限
    @Column(nullable = false)
    private long depositLimit;

    // 存款期限
    @Column(nullable = false)
    private Timestamp depositTerm;

    // 年利率
    @Column(nullable = false)
    private double apr;

    // 是否当日起息
    @Column(nullable = false)
    private boolean onDay;

    // 是否随存随取
    @Column(nullable = false)
    private boolean dawa;


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
    private LoanRule ruler;
}
