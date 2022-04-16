package com.moflowerlkh.decisionengine.domain.entities.rules;

import lombok.*;
import org.hibernate.Hibernate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EntityListeners;
import javax.persistence.Table;
import java.sql.Timestamp;
import java.util.Objects;

/**
 * @Description 秒杀规则 商品 1 - 1 活动
 */
@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Table(name = "loan_rule")
@EntityListeners(AuditingEntityListener.class)
public class LoanRule extends BaseRule {

    //购买人数限制
    @Column
    private Long purchasersNumberLimit;

    // 分几期
    @Column(nullable = false)
    private String timeLimit;

    // 还几年
    @Column
    private Integer replayLimit;

    // 年利率
    @Column(nullable = false)
    private double apr;

    //贷款额度上限
    @Column
    private Long maxMoneyLimit;
    // 贷款额度下限
    @Column
    private Long minMoneyLimit;

    // 贷款时间
    @Column(nullable = true)
    private Timestamp MaxTime;
    @Column(nullable = true)
    private Timestamp MinTime;

    // 是否需要担保
    @Column
    private Boolean checkGuarantee;

    // 检查就业状况
    @Column(nullable = true)
    private Boolean checkEmployment;

    // 检查是否是失信人员
    @Column(nullable = true)
    private Boolean checkDishonest;

    // 检查是否逾期
    @Column(nullable = true)
    private Boolean checkOverDual;

    // 是否需要抵押
    @Column
    private Boolean checkPledge;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        LoanRule loanRule = (LoanRule) o;
        return getId() != null && Objects.equals(getId(), loanRule.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
