package com.moflowerlkh.decisionengine.domain.entities;

import lombok.*;
import org.hibernate.Hibernate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.persistence.*;
import java.util.Objects;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Getter
@Setter
@ToString
@Entity
@Table(name = "user_activity")
@EntityListeners(AuditingEntityListener.class)
public class UserActivity extends BasePO {

    private Long userId;

    private Long activityId;

    private Boolean isPassed;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        UserActivity that = (UserActivity) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
