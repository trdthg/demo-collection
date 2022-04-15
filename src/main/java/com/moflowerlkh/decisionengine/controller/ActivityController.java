package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.service.ActivityService;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponseDTO;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.List;


@RestController
@Api(tags = {"活动结果"})
@RequestMapping("/api/activity")
public class ActivityController {

    @Autowired
    ActivityService activityService;

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
