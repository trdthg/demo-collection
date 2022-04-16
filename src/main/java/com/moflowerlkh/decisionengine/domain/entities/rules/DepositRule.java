package com.moflowerlkh.decisionengine.domain.entities.rules;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EntityListeners;
import javax.persistence.Table;
import java.sql.Timestamp;
import java.util.Date;
import java.util.Objects;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

/**
 * @Description 秒杀规则 商品 1 - 1 活动
 */
@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Table(name = "deposit_rule")
@EntityListeners(AuditingEntityListener.class)
public class DepositRule extends BaseRule {

    //购买人数限制
    @Column
    private Long purchasersNumberLimit;

    // 存款期限
    @Column(nullable = false)
    private String timeLimit;

    // 年利率
    @Column(nullable = false)
    private double apr;

    // 检查就业状况
    @Column(nullable = true)
    private Boolean checkEmployment;

    // 检查是否是失信人员
    @Column(nullable = true)
    private Boolean checkDishonest;

    // 是否当日起息
    @Column(nullable = false)
    private Boolean isOnDay;

    // 是否随存随取
    @Column(nullable = false)
    private Boolean idDawa;

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
