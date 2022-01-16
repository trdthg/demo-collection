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
    @Column(name = "id", nullable = false)
    private Long id;

    // 贷款额度
    @Column(nullable = false)
    private boolean checkMaxMoney;
    @Column()
    private long MaxMoney;

    @Column(nullable = false)
    private boolean checkMinMoney;
    @Column()
    private long MinMoney;

    // 贷款时间
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
    private boolean checkMaxAge;
    @Column()
    private int MaxAge;

    @Column(nullable = false)
    private boolean checkMinAge;
    @Column()
    private int MinAge;

    // 检查就业状况
    @Column(nullable = false)
    private boolean checkEmployment;
    @Transient
    private List<Employment> allowedEmployments;

    // 检查是否是失信人员
    @Column(nullable = false)
    private boolean checkDishonest;

    // 检查是否逾期
    @Column(nullable = false)
    private boolean checkOverDual;

    // 是否限制地区
    @Column(nullable = false)
    private boolean checkCountry;
    @Transient
    private List<String> allowedCountries;

    // 对应的活动
    @JoinColumn(nullable = false)
    @OneToOne
    private LoanActivity loanActivity;
}
