package com.moflowerlkh.decisionengine.entity;

import lombok.Data;

import javax.persistence.*;
import java.sql.Timestamp;
import java.util.List;

/**
 * @Description 秒杀规则  商品 1 - 1 活动
 */
@Entity
@Data
@Table(name = "ruler_tb")
public class DepositRule {
    @Id
    @Column(name = "id", nullable = false)
    private Long id;

    // 存/贷款 额度
    @Column(nullable = false)
    private boolean checkMaxMoney;
    @Column()
    private long MaxMoney;

    @Column(nullable = false)
    private boolean checkMinMoney;
    @Column()
    private long MinMoney;

    //存/贷款 时间
    @Column(nullable = false)
    private boolean checkMaxTime;
    @Column()
    private Timestamp MaxTime;

    @Column(nullable = false)
    private boolean checkMinTime;
    @Column()
    private Timestamp MinTime;

    // 检查年龄
    @Column(nullable = false)
    private boolean checkAge;
    @Column()
    private int MaxAge;
    @Column()
    private int MinAge;

    // 是否限制地区
    @Column(nullable = false)
    private boolean checkCountry;
    @Column()
    private List<String> allowedCountries;

    // 对应的活动
    @JoinColumn(nullable = false)
    @OneToOne
    private DepositActivity depositActivity;
}
