package com.moflowerlkh.decisionengine.controller;

import com.fasterxml.jackson.databind.exc.UnrecognizedPropertyException;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import org.springframework.boot.json.JsonParseException;
import org.springframework.context.support.DefaultMessageSourceResolvable;
import org.springframework.dao.DataAccessException;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageConversionException;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Arrays;
import java.util.Objects;
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

    @ExceptionHandler(DataAccessException.class)
    @ResponseBody
    public BaseResponse<String> DataAccessExceptionHandler(DataAccessException e){
        if (e instanceof DataIntegrityViolationException) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "字段不能重复: " + Objects.requireNonNull(e.getRootCause()).getMessage());
        } else if (e instanceof DataRetrievalFailureException) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "数据获取失败: " + e.getMessage());
        } else {
            return new BaseResponse<>(HttpStatus.INTERNAL_SERVER_ERROR, "数据库未知异常: " + e.getMessage());
        }
    }

    @ExceptionHandler(HttpMessageConversionException.class)
    @ResponseBody
    public BaseResponse<String> HttpMessageConversionException(HttpMessageConversionException e) {
        if (e instanceof HttpMessageNotReadableException) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "参数格式不匹配: " + e.getMessage());
        } else {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "参数格式不匹配: " + e.getMessage());
        }
    }

    @ExceptionHandler(Exception.class)
    @ResponseBody
    public BaseResponse<String> UnknownExceptionHandler(Exception e) {
        e.printStackTrace();
        return new BaseResponse<String>(HttpStatus.INTERNAL_SERVER_ERROR, "服务端异常: " + e.getMessage());
    }
}