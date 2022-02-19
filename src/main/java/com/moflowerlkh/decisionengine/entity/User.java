package com.moflowerlkh.decisionengine.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.Gender;
import lombok.*;
import org.hibernate.Hibernate;
import org.hibernate.validator.constraints.Length;

import javax.persistence.*;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Entity
@Table(name = "user_tb")
public class User {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = true)
    @Length(min = 1, max = 64)
    private String name;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = true)
    @Min(value = 0)
    @Max(value = 9999)
    private Integer age;

    @Column(nullable = true)
    @Enumerated(EnumType.STRING)
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
    private Long overDual;

    // 就业状态
    @Column(nullable = true)
    @Enumerated(EnumType.STRING)
    private Employment employment;

    // 被列入失信人名单
    @Column(nullable = true)
    private Boolean dishonest;

    @JsonIgnoreProperties(value = {"users"})
    @ManyToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @Column(nullable = true)
    private Set<LoanActivity> loanActivities = new HashSet<LoanActivity>();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        User user = (User) o;
        return id != null && Objects.equals(id, user.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}


