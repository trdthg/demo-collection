package com.moflowerlkh.decisionengine.vo;

import lombok.Data;
import org.springframework.http.HttpStatus;

@Data
public class BaseResponse<T> {
    int code;
    T content;
    String message;

    public BaseResponse() {
        this.code = 200;
        this.content = null;
        this.message = "成功";
    }

    public BaseResponse(int code) {
        this.code = code;
        this.content = null;
        if (code == 404) {
            this.message = "反正就是404";
        }
    }

    public BaseResponse(int code, String message) {
        this.code = code;
        this.content = null;
        this.message = message;
    }

    public BaseResponse(T content) {
        this.code = 200;
        this.content = content;
        this.message = "成功";
    }

    public BaseResponse(int code, T content, String message) {
        this.code = code;
        this.content = content;
        this.message = message;
    }

    public BaseResponse(HttpStatus httpStatus, String message) {
        this.code = httpStatus.value();
        this.message = message;
        this.content = null;
    }

    public BaseResponse(HttpStatus httpStatus, String message, T content) {
        this.code = httpStatus.value();
        this.message = message;
        this.content = content;
    }
}