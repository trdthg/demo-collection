package com.moflowerlkh.decisionengine.entity;

import lombok.Data;
import org.hibernate.annotations.OnDelete;

import javax.persistence.*;
import java.sql.Timestamp;

@Entity
@Data
@Table(name = "loan_activity_tb")
public class LoanActivity {
    @Id
    @Column(name = "id", nullable = false)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    // 统一使用 2022-01-01 20:00:00 时间格式
    @Column(nullable = false)
    private Timestamp beginTime;

    @Column(nullable = false)
    private Timestamp endTime;

    // 贷款额度上限
    @Column(nullable = false)
    private double maxMoneyLimit;

    @Column()
    private double minMoneyLimit;

    // 分几期
    @Column(nullable = false)
    private String timeLimit;
    // 还几年
    @Column
    private String replayLimit;

    // 年利率
    @Column(nullable = false)
    private double apr;

    /**
     * 一个秒杀活动只能对应一个商品
     * 一个商品可能有多个秒杀活动
     */
    @JoinColumn(nullable = false)
    @ManyToOne(cascade = CascadeType.MERGE, fetch = FetchType.EAGER)
    private ShoppingGoods shoppingGoods;

    // 活动销售总数，不能超卖
    @Column(nullable = false)
    private long shoppingTotal;

    // 对应的规则
    // 一个活动对应一个规则
    @OneToOne(cascade = CascadeType.ALL)
    private LoanRule rule;
}
