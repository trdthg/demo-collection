package com.moflowerlkh.decisionengine.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.*;
import java.sql.Timestamp;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@Getter
@Setter
@ToString
@Entity
@RequiredArgsConstructor
@Table(name = "loan_activity_tb")
public class LoanActivity {
    @Id
    @Column(name = "id", nullable = false)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 活动名称
    @Column(nullable = false)
    private String name;

    // 活动开始时间，统一使用 2022-01-01 20:00:00 时间格式
    @Column(nullable = false)
    private Timestamp beginTime;
    // 活动结束时间
    @Column(nullable = false)
    private Timestamp endTime;

    // 贷款额度上限
    @Column()
    private double maxMoneyLimit;
    // 贷款额度下限
    @Column()
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

    /**
     * 一个秒杀活动只能对应一个商品
     * 一个商品可能有多个秒杀活动
     */
    // @JoinColumn(nullable = false)
    // @ManyToOne(fetch = FetchType.EAGER)
    // private ShoppingGoods shoppingGoods;

    // 活动销售总数，不能超卖
    @Column(nullable = false)
    private long amount;

    // 总共可贷款金额
    @Column(nullable = false)
    private long moneyTotal;

    // 活动对应的规则，一个活动对应一个规则
    @JoinColumn(nullable = true)
    @OneToOne(cascade = { CascadeType.ALL }, fetch = FetchType.EAGER)
    private LoanRule rule;

    @OneToMany(mappedBy = "loanActivity", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    private Set<UserLoanActivity> userLoanActivities = new HashSet<>();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        LoanActivity that = (LoanActivity) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
