package com.moflowerlkh.decisionengine.entity;

import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.Gender;
import lombok.Data;
import org.hibernate.annotations.ColumnDefault;
//import org.hibernate.annotations.*;

import javax.persistence.*;

@Data
@Entity
@Table(name = "user_tb")
public class User {
    @Id
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private Integer age;

    @Column(nullable = false)
    @Enumerated(EnumType.ORDINAL)
    private Gender gender;

    // 年收入信息
    @Column(nullable = false)
    private Long yearIncome;

    // 身份证号
    @Column(nullable = false)
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
    @Column(nullable = false)
    private long overDual;

    // 就业状态
    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private Employment employment;

    // 被列入失信人名单
    @Column(nullable = false)
    private boolean dishonest;
}


