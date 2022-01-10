package com.moflowerlkh.decisionengine.model;

import lombok.Data;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Data
@Entity
@Table(name = "user_tb")
public class User {
    @Id
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;

    // 性别
    @Column(nullable = false)
    private String gender;

    // 年收入信息
    @Column(nullable = false)
    private long yearIncome;

    // 其他信息
}
