package com.moflowerlkh.decisionengine.entity;

import lombok.Data;

import javax.persistence.*;
import java.util.List;
import java.util.Set;

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

    //@OneToMany(cascade = CascadeType.ALL, fetch = FetchType.LAZY) //一对多为Lazy，多对一为Eager
    //private List<LoanActivity> loanActivities;

    //@OneToMany(cascade={CascadeType.ALL}, fetch=FetchType.LAZY) //一对多为Lazy，多对一为Eager
    //@JoinColumn() //name=定义外键在本表的字段名
    //private Set<DepositActivity> depositActivities;

}
