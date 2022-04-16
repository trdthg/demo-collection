package com.moflowerlkh.decisionengine.domain.entities;

import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.enums.Gender;
import lombok.*;
import org.hibernate.Hibernate;
import org.hibernate.validator.constraints.Length;

import javax.persistence.*;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@RequiredArgsConstructor
@Getter
@Setter
@ToString
@Entity
@Table(name = "user")
public class User extends BasePO {

    // 姓名
    @Column(name = "name", nullable = false)
    @Length(min = 1, max = 64)
    private String name;

    // 用户名
    @Column(name = "username", nullable = false, unique = true)
    private String username;

    // 密码
    @Column(nullable = false)
    private String password;

    // 年龄
    @Column(nullable = false)
    @Min(value = 0)
    @Max(value = 9999)
    private Integer age;

    // 性别
    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private Gender gender;

    // 年收入信息
    @Column(nullable = true)
    private Long yearIncome;

    // 身份证号
    @Column(nullable = false, unique = true)
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

    // 用户拥有的角色
    @ElementCollection(fetch = FetchType.EAGER)
    @Column(nullable = true)
    private Set<String> roles = new HashSet<String>();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        User user = (User) o;
        return getId() != null && Objects.equals(getId(), user.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
