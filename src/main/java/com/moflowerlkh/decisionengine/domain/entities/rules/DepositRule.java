package com.moflowerlkh.decisionengine.domain.entities.rules;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.Column;
import javax.persistence.Entity;
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
@Table(name = "deposit_rule_tb")
public class DepositRule extends BaseRule {

    // 存/贷款 额度
    @Column(nullable = false)
    private boolean checkMaxMoney;
    @Column()
    private long MaxMoney;

    @Column(nullable = false)
    private boolean checkMinMoney;
    @Column()
    private long MinMoney;

    // 存/贷款 时间
    @Column(nullable = false)
    private boolean checkMaxTime;
    @Column()
    private Timestamp MaxTime;

    @Column(nullable = false)
    private boolean checkMinTime;
    @Column()
    private Timestamp MinTime;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        DepositRule that = (DepositRule) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
