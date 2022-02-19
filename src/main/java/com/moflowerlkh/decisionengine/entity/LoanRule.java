package com.moflowerlkh.decisionengine.entity;

import com.moflowerlkh.decisionengine.enums.Employment;
import lombok.Data;

import javax.persistence.*;
import java.sql.Timestamp;
import java.util.List;

/**
 * @Description 秒杀规则  商品 1 - 1 活动
 */
@Entity
@Data
@Table(name = "loan_rule_tb")
public class LoanRule {
    @Id
    @Column(name = "id", nullable = true)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 贷款额度
    @Column(nullable = true)
    private long checkMaxMoney;

    @Column(nullable = true)
    private long checkMinMoney;

    // 贷款时间
    @Column(nullable = true)
    private Timestamp MaxTime;

    @Column(nullable = true)
    private Timestamp MinTime;

    // 检查年龄
    @Column(nullable = true)
    private int MaxAge;

    @Column(nullable = true)
    private int MinAge;

    // 是否需要担保
    @Column
    private boolean checkGuarantee;

    // 检查就业状况
    @Column(nullable = true)
    private boolean checkEmployment;

    // 检查是否是失信人员
    @Column(nullable = true)
    private boolean checkDishonest;

    // 检查是否逾期
    @Column(nullable = true)
    private boolean checkOverDual;

    // 是否需要抵押
    @Column
    private boolean checkPledge;

    // 是否限制地区
    @Column(nullable = true)
    private boolean checkCountry;

    //// 对应的活动
    //@JoinColumn(nullable = true)
    //@OneToOne(cascade = CascadeType.ALL)
    //private LoanActivity loanActivity;
}
