package com.moflowerlkh.decisionengine.service.ActivityServiceDTO;

import com.moflowerlkh.decisionengine.domain.entities.OrderResultEnum;
import lombok.Builder;
import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import javax.persistence.Column;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import java.util.Date;

@Data
@Builder
public class GetOrdersResponse {
    private Long user_id;
    private Long activity_id;
    private Long goods_id;
    private Long order_id;

    private String activity_name;
    private Long bank_account;
    private Long goods_price;
    private OrderResultEnum order_result;

    private String create_time;
}
