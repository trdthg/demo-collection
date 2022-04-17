package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.component.RequestLimiter;
import com.moflowerlkh.decisionengine.domain.dao.UserDao;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.service.ActivityService;
import com.moflowerlkh.decisionengine.service.ActivityServiceDTO.GetOrdersResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponseDTO;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.List;
import java.util.concurrent.TimeUnit;


@RestController
@Api(tags = {"活动结果"})
@RequestMapping("/api/activity")
public class ActivityController {

    @Autowired
    ActivityService activityService;
    @Autowired
    UserDao userDao;

    @GetMapping("/{activity_id}/passed")
    @ApiOperation("查询-初筛通过")
    public BaseResponse getLoanActivityByIdA(
        @Valid @NotNull @PathVariable Long activity_id,
        String name
    ) {
        if (name != null) {
            return activityService.getPassedUser(activity_id, name);
        }
        return activityService.getPassedUsers(activity_id);
    }

    @GetMapping("/{activity_id}/unpassed")
    @ApiOperation("查询-初筛不通过")
    public BaseResponse getLoanActivityByIdB(
        @Valid @NotNull @PathVariable Long activity_id,
        String name
    ) {
        if (name != null && name.isEmpty()) {
            return activityService.getUnpassedUser(activity_id, name);
        }
        return activityService.getUnPassedUsers(activity_id);
    }

    @GetMapping("/orders")
    @ApiOperation("查询订单")
    public BaseResponse getRecords(String username) {
        if (username == null) {
            return new BaseResponse(HttpStatus.OK, "您需要提供姓名", null);
        }
        User user = userDao.findByUsername(username);
        if (user == null) {
            return new BaseResponse(HttpStatus.OK, "查询用户失败", null);
        }
        List<GetOrdersResponse> res = activityService.findOrders(user);
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }

    //@GetMapping("/{activity_id}/passed")
    //@ApiOperation("查询通过-根据用户名字")
    //public BaseResponse<JoinLoanActivityUserResponseDTO> ifUserPassed(@Valid @NotNull @PathVariable Long activity_id,
    //                                                                  @RequestParam String name) throws Exception {
    //    return activityService.getPassedUser(activity_id, name);
    //}
    //
    //@GetMapping("/{activity_id}/unpassed")
    //@ApiOperation("查询未通过-根据用户名字")
    //public BaseResponse<JoinLoanActivityUserResponseDTO> ifUserUnPassed(@Valid @NotNull @PathVariable Long activity_id,
    //                                                                    @RequestParam String name) throws Exception {
    //}
}
