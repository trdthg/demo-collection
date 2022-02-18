package com.moflowerlkh.decisionengine.entity;

import lombok.Data;

import javax.persistence.*;

/**
 * 秒杀商品
 */
@Entity
@Data
@Table(name = "shopping_goods_tb")
public class ShoppingGoods {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = true)
    private String info;

    // 商品总数
    @Column(nullable = false)
    private Long goodsTotal;

}
