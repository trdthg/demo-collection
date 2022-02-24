package com.moflowerlkh.decisionengine.vo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BaseResult<T> {
    T result;
    String message;
}
