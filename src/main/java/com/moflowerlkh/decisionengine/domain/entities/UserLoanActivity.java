package com.moflowerlkh.decisionengine.domain.entities;

import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import lombok.*;
import org.hibernate.Hibernate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;
import java.util.Objects;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Getter
@Setter
@ToString
@Entity
@Table(name = "user_loan_activity_tb")
@EntityListeners(AuditingEntityListener.class)
public class UserLoanActivity extends BasePO {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id")
    @ToString.Exclude
    private User user;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "loanActivity_id")
    @ToString.Exclude
    private LoanActivity loanActivity;

    private Boolean isPassed;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        UserLoanActivity that = (UserLoanActivity) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
