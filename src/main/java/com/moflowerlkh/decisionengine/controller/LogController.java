package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.domain.entities.Log;
import com.moflowerlkh.decisionengine.domain.dao.LogDao;
import com.moflowerlkh.decisionengine.vo.BaseResponse;

//import io.micrometer.core.annotation.Counted;
//import io.micrometer.core.annotation.Timed;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.Date;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@RestController
@Api(tags = { "日志相关" })
@RequestMapping("/api/log")
public class LogController {

    @Autowired
    LogDao LogDao;

    @PostMapping("/")
    @ResponseBody
    @ApiOperation(value = "新增日志", notes = "新增一个日志")
    public BaseResponse<Log> post(@RequestBody @Valid PostLogRequest request) {
        Log Log = request.into();
        LogDao.save(Log);
        return new BaseResponse<>(HttpStatus.CREATED, "新增日志成功", Log);
    }

    @PutMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "编辑日志", notes = "根据 id 修改日志信息")
    public BaseResponse<Log> put(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id,
            @RequestBody @Valid PostLogRequest request) {
        Log Log = request.into();
        Log.setId(id);
        LogDao.saveAndFlush(Log);
        return new BaseResponse<>(HttpStatus.CREATED, "修改日志成功", Log);
    }

    @GetMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "查询日志", notes = "根据 id 查找日志信息")
    public BaseResponse<Log> put(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id) {
        Log Log = LogDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("查询结果为空，没有该日志"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", Log);
    }

    @DeleteMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "删除日志", notes = "根据 id 删除日志")
    public BaseResponse<String> delete(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id) {
        LogDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", null);
    }
}

@Data
class PostLogRequest {

    @NotEmpty(message = "标题不能为空")
    private String title;

    @NotEmpty(message = "内容不能为空")
    private String content;

    @NotEmpty(message = "类型不能为空")
    private String type;

    public Log into() {
        Log log = new Log();
        log.setCreateDate(new Date());

        log.setTime(new Date());
        log.setType(type);
        log.setTitle(title);
        log.setContent(content);
        return log;
    }
}