package com.moflowerlkh.decisionengine.domain.entities;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;

import java.util.Date;
import java.util.Objects;

/**
 * 日志
 */
@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
@Table(name = "loggg")
public class Log extends BasePO {
    @Column(nullable = true)
    private String content;
    @Column(nullable = false)
    private String title;
    @Column(nullable = false)
    private String type;
    @Column(nullable = false)
    private Date time;

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o))
            return false;
        Goods that = (Goods) o;
        return getId() != null && Objects.equals(getId(), that.getId());
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
