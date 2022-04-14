package com.moflowerlkh.decisionengine.domain.entities;

import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import lombok.*;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Getter
@Setter
@ToString
@Entity
@Table(name = "user_deposit_activity_tb")
@EntityListeners(AuditingEntityListener.class)
public class UserDepositActivity extends BasePO {

    private Long userId;

    private Long activityId;

    private Boolean isPassed;
}
