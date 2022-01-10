package com.moflowerlkh.decisionengine.model;

import lombok.Data;

import javax.persistence.*;

@Entity
@Data
@Table(name = "ruler_tb")
public class Ruler {
    @Id
    @Column(name = "id", nullable = false)
    private Long id;

    /**
     * 规则一是否生效标志
     */
    @Column(nullable = false)
    private boolean rulerOne;

    // 对应的活动
    @Column(nullable = false)
    @OneToOne
    private ShoppingActivity shoppingActivity;
}
