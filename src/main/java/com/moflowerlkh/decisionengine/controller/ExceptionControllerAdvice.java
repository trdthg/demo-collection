package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.vo.BaseResponse;
import org.springframework.context.support.DefaultMessageSourceResolvable;
import org.springframework.dao.DataAccessException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Arrays;
import java.util.stream.Stream;

/**
 * 统一参数校验失败时的处理
 */
@RestControllerAdvice
public class ExceptionControllerAdvice {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public BaseResponse<String> MethodArgumentNotValidExceptionHandler(MethodArgumentNotValidException e) {
        // 从异常对象中拿到ObjectError对象
        String mes = e.getBindingResult().getAllErrors().get(0).getDefaultMessage();
        // 然后提取错误提示信息进行返回
        return new BaseResponse<String>(HttpStatus.BAD_REQUEST, "参数不合法: " + mes);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseBody
    public BaseResponse<String> MethodIllegalArgumentExceptionHandler(IllegalArgumentException e) {
        return new BaseResponse<String>(HttpStatus.BAD_REQUEST, "参数异常: " + e.getMessage());
    }

    @ExceptionHandler(Exception.class)
    @ResponseBody
    public BaseResponse<String> MethodUnknownExceptionHandler(Exception e) {
        return new BaseResponse<String>(HttpStatus.INTERNAL_SERVER_ERROR, "服务端异常: " + e.getMessage());
    }

    @ExceptionHandler(DataAccessException.class)
    @ResponseBody
    public BaseResponse<String> DataAccessExceptionHandler(DataAccessException e){
        if (e instanceof DataIntegrityViolationException) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "重复: " + e.getMessage());
        } else {
            return new BaseResponse<>(HttpStatus.INTERNAL_SERVER_ERROR, "数据库执行异常: ", e.getMessage());
        }
    }
}