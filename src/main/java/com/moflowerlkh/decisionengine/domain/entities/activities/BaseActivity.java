package com.moflowerlkh.decisionengine.domain.entities.activities;

import com.moflowerlkh.decisionengine.domain.entities.BasePO;
import lombok.*;

import javax.persistence.Column;
import javax.persistence.MappedSuperclass;

import java.sql.Timestamp;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@MappedSuperclass
public class BaseActivity extends BasePO {
    // 活动名称
    @Column(nullable = false)
    private String name;

    // 活动开始时间，统一使用 2022-01-01 20:00:00 时间格式
    @Column(nullable = false)
    private Timestamp beginTime;
    // 活动结束时间
    @Column(nullable = false)
    private Timestamp endTime;

    /**
     * 一个秒杀活动只能对应一个商品
     * 一个商品可能有多个秒杀活动
     */
    // @JoinColumn(nullable = false)
    // @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    private Long goodsId;
}
