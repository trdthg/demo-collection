package com.moflowerlkh.decisionengine.domain;


import com.moflowerlkh.decisionengine.domain.entities.BasePO;
import com.moflowerlkh.decisionengine.domain.entities.OrderResultEnum;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;

@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class GoodsOrder extends BasePO {
    /**
     * 商品标识，由数据库生成，用于查询商品详细属性，要求商品表不能执行删除，保存历史，用字段标识下架。
     */
    @Column(name = "goods_id", nullable = false)
    private long goodsID;

    /**
     * 银行账户标识，不采用数据库生成 ID，用于查询扣款账户。
     */
    @Column(name = "bank_account_sn", nullable = false)
    private long bankAccountSN;

    /**
     * 商品价格，不同订单可能由于购买时间不同，价格不同，需要同订单一同记录。
     */
    @Column(name = "goods_price", nullable = false)
    private long goodsPrice;

    /**
     * 下单结果
     * 枚举类
     * SUCCESS(1, "下单成功"),
     * FAILED(2, "下单失败"),
     * BALANCE_NOT_ENOUGH(3, "余额不足"),
     * GOODS_NOT_ENOUGH(4, "商品库存不足"),
     * ;
     */
    @Enumerated(EnumType.STRING)
    @Column(name = "order_reuslt", nullable = false)
    private OrderResultEnum orderResultEnum;

    public static GoodsOrder New(long goodsID, long goodsPrice, long bankAccountSN, OrderResultEnum orderResultEnum) {
        GoodsOrder goodsOrder = new GoodsOrder();
        goodsOrder.setGoodsID(goodsID);
        goodsOrder.setGoodsPrice(goodsPrice);
        goodsOrder.setBankAccountSN(bankAccountSN);
        goodsOrder.setOrderResultEnum(orderResultEnum);
        return goodsOrder;
    }
}

