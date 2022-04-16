package com.moflowerlkh.decisionengine.domain.entities;


import lombok.Getter;

@Getter
public enum OrderResultEnum {
    INIT(0, "正在处理订单"),
    SUCCESS(1, "订单完成"),
    FAILED(2, "订单失败"),
    BALANCE_NOT_ENOUGH(3, "余额不足"),
    GOODS_NOT_ENOUGH(4, "商品库存不足"),
    ;

    Integer id;

    String description;

    OrderResultEnum(int id, String description) {
        this.id = id;
        this.description = description;
    }
}
