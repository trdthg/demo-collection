package com.moflowerlkh.decisionengine.domain.entities.rules;

import com.moflowerlkh.decisionengine.domain.entities.BasePO;
import com.moflowerlkh.decisionengine.domain.entities.activities.BaseActivity;
import com.moflowerlkh.decisionengine.domain.entities.activities.DepositActivity;
import lombok.*;

import javax.persistence.*;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@MappedSuperclass
public class BaseRule extends BasePO {
    // 检查年龄
    @Column()
    private Integer MaxAge;

    @Column()
    private Integer MinAge;

    // 是否限制地区
    @Column(nullable = true)
    private Boolean checkCountry;

    // // 对应的活动
    // @JoinColumn(nullable = false)
    // @OneToOne
    // private BaseActivity activity;
}
