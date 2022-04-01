package com.moflowerlkh.decisionengine.domain.entities;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import javax.persistence.*;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.util.Date;

@Getter
@Setter
@ToString
@RequiredArgsConstructor
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public class BasePO {
    @Id
    @Column(nullable = false, unique = true)
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @CreatedDate
    @Column(name = "create_time")
    private Date createDate;

    @LastModifiedDate
    @Column(name = "modify_time")
    private Date modifyDate;

}
