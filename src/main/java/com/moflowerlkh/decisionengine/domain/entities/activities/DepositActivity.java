package com.moflowerlkh.decisionengine.domain.entities.activities;

import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;
import lombok.Data;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * 秒杀规则 1 - 1 秒杀活动 - +
 * |-- 商品
 *
 * @Description 秒杀活动 秒杀规则 1 - 1 秒杀活动 - +
 */
@Entity
@RequiredArgsConstructor
@Getter
@Setter
@ToString
@Table(name = "deposit_activity_tb")
public class DepositActivity extends BaseActivity {
    // 存款额度下限
    @Column(nullable = false)
    private long depositLimit;

    // 存款期限
    @Column(nullable = false)
    private Timestamp depositTerm;

    // 年利率
    @Column(nullable = false)
    private double apr;

    // 是否当日起息
    @Column(nullable = false)
    private boolean onDay;

    // 是否随存随取
    @Column(nullable = false)
    private boolean dawa;

    // 活动销售总数，不能超卖
    @Column(nullable = false)
    private long shoppingTotal;

    // 对应的规则
    @JoinColumn(nullable = false)
    @OneToOne
    private DepositRule rule;
}
