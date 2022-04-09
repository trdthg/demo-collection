package com.moflowerlkh.decisionengine.domain.entities;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import java.util.Objects;

@Entity
@Getter
@Setter
@ToString
@Table(name = "bank_account")
public class BankAccount extends BasePO {

    /**
     * 银行账号标识，要求全球唯一。
     */
    @Column(name = "bank_account_sn", unique = true, nullable = false)
    private long bankAccountSN;

    /**
     * 用户
     * user_id is relative to user_tb
     */
    @Column(name = "user_id", nullable = false)
    private long userID;

    /**
     * 银行余额
     */
    @Column(name = "balance", nullable = false)
    private long balance;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        BankAccount that = (BankAccount) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
