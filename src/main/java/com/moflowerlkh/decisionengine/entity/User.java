package com.moflowerlkh.decisionengine.entity;

import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.Gender;
import lombok.Data;
import org.hibernate.annotations.Check;
import org.hibernate.annotations.GenericGenerator;
//import org.hibernate.annotations.*;

import javax.persistence.*;

@Data
@Entity
@Table(name = "user_tb")
public class User {
    @Id
    @GenericGenerator(name = "这是什么", strategy = "increment")
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = true)
    private String password;

    @Column(nullable = true)
    @Check(constraints = "age < 200 and age >= 0")
    private Integer age;

    @Column(nullable = true)
    @Enumerated(EnumType.ORDINAL)
    private Gender gender;

    // 年收入信息
    @Column(nullable = true)
    private Long yearIncome;

    // 身份证号
    @Column(nullable = true)
    private String IDNumber;

    // 国家
    @Column(nullable = true)
    private String country;
    // 省份
    @Column(nullable = true)
    private String province;
    // 城市
    @Column(nullable = true)
    private String city;

    // 近三年逾期还款数
    @Column(nullable = true)
    private long overDual;

    // 就业状态
    @Column(nullable = true)
    @Enumerated(EnumType.ORDINAL)
    private Employment employment;

    // 被列入失信人名单
    @Column(nullable = true)
    private boolean dishonest;
}


