package com.moflowerlkh.decisionengine.domain.entities.activities;

import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;
import lombok.*;

import javax.persistence.*;
import java.sql.Timestamp;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

/**
 * 秒杀规则 1 - 1 秒杀活动 - +
 * |-- 商品
import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;
import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;
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

    //名称
    @Column(nullable = false)
    private String name;

    // 存款期限
    @Column(nullable = false)
    private String timeLimit;

    // 年利率
    @Column(nullable = false)
    private double apr;

    @Column(nullable = false)
    private Long depositRuleId;

    @ElementCollection
    private Set<Long> userIds = new HashSet<>();

}
