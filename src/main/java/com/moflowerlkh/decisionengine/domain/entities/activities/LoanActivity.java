package com.moflowerlkh.decisionengine.domain.entities.activities;

import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;
import lombok.*;
import org.hibernate.Hibernate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@RequiredArgsConstructor
@Getter
@Setter
@ToString
@Table(name = "loan_activity_tb")
@Entity
@EntityListeners(AuditingEntityListener.class)
public class LoanActivity extends BaseActivity {

    // 贷款额度上限
    @Column
    private double maxMoneyLimit;
    // 贷款额度下限
    @Column
    private double minMoneyLimit;

    // 分几期
    @Column(nullable = false)
    private String timeLimit;

    // 还几年
    @Column
    private Integer replayLimit;

    // 年利率
    @Column(nullable = false)
    private double apr;

    // 总共可贷款金额
    @Column(nullable = false)
    private long moneyTotal;

    // 活动对应的规则，一个活动对应一个规则
    // @JoinColumn(nullable = true)
    // @OneToOne(cascade = { CascadeType.ALL }, fetch = FetchType.EAGER)
    // private LoanRule rule;
    @Column
    private Long loanRuleId;

    @OneToMany(mappedBy = "loanActivity", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    private Set<UserLoanActivity> userLoanActivities = new HashSet<>();

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        LoanActivity that = (LoanActivity) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
