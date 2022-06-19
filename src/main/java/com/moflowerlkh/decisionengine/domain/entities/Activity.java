package com.moflowerlkh.decisionengine.domain.entities;

import com.moflowerlkh.decisionengine.domain.dao.UserDao;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponseDTO;
import lombok.*;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;

import java.sql.Timestamp;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Getter
@Setter
@ToString
@Table(name = "activity")
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Activity extends BasePO {
    // 活动名称
    @Column(nullable = false)
    private String name;

    // 活动开始时间，统一使用 2022-01-01 20:00:00 时间格式
    @Column(nullable = false)
    private Timestamp beginTime;
    // 活动结束时间
    @Column(nullable = false)
    private Timestamp endTime;

    // 商品 id
    private Long goodsId;

    // 规则 ID
    private Long ruleId;

    // 活动类型
    private Integer type;
}
