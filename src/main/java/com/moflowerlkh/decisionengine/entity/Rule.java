package com.moflowerlkh.decisionengine.entity;

import lombok.Data;
import org.hibernate.annotations.Check;
import reactor.util.annotation.Nullable;

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
    @JoinColumn(nullable = false)
    @OneToOne
    private ShoppingActivity shoppingActivity;
}
