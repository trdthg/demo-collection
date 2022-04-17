package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.component.AccessLimiter;
import com.moflowerlkh.decisionengine.component.RequestLimiter;
import com.moflowerlkh.decisionengine.domain.entities.Activity;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.CreateDepositActivityRequestDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.CreateDepositActivityResponseDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.GetActivityResponseDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityService;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.TryJoinResponseDTO;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.List;

@RestController
@Api(tags = {"Deposit 存款活动"})
@RequestMapping("/api/deposit")
public class DepositActivityController {
    @Autowired
    DepositeActivityService depositeActivityService;

    @PostMapping("/")
    @ApiOperation(value = "新增", notes = "创建一个新活动，同时会创建一个新商品，商品购买后的所得金额会进入创建者的账户")
    public BaseResponse<GetActivityResponseDTO> create(@RequestBody @Valid CreateDepositActivityRequestDTO request) {
        return depositeActivityService.create(request);
    }

    @PutMapping("/{id}")
    @ApiOperation(value = "修改-全部", notes = "需要传完整，传来的信息会直接全部覆盖掉原来的")
    public BaseResponse<GetActivityResponseDTO> update(@Valid @NotNull @PathVariable Long id,
                                                                  @RequestBody @Valid CreateDepositActivityRequestDTO request) {
        return depositeActivityService.update(id, request);
    }

    @GetMapping("/")
    @ApiOperation(value = "分页查询", notes = "活动的基本信息")
    public BaseResponse<PageResult<List<GetActivityResponseDTO>>> getLoanActivityByIdSimple(
        @RequestParam Integer page_num, @RequestParam Integer page_limit) {
        return depositeActivityService.findByPage(page_num, page_limit);
    }

    @GetMapping("/{id}")
    @ApiOperation(value = "查询", notes = "不带有活动的参加信息")
    public BaseResponse<GetActivityResponseDTO> getLoanActivityByIdSimple(@Valid @NotNull @PathVariable Long id) {
        return depositeActivityService.findById(id);
    }

    @DeleteMapping("/{id}")
    @ApiOperation("删除")
    public BaseResponse<Boolean> deleteLoanActivityById(@Valid @NotNull @PathVariable Long id) {
        return depositeActivityService.deleteById(id);
    }

    @GetMapping("/check")
    @ApiOperation("初筛")
    public BaseResponse<Boolean> check(@Valid @NotNull Long user_id, @Valid @NotNull Long activity_id) {
        return depositeActivityService.check(user_id, activity_id);
    }

    @AccessLimiter(key = "deposit_join", limit = 10, timeout = 2)
    @RequestLimiter(QPS = 300, timeout = 1)
    @GetMapping("/join")
    @ApiOperation(value = "参加活动", notes = "")
    public BaseResponse<TryJoinResponseDTO> joinLoanActivity(@Valid @NotNull Long activity_id,
                                                             @Valid @NotNull Long user_id,
                                                             @Valid @NotNull String account_id)
        throws Exception {
        return depositeActivityService.tryJoin(activity_id, user_id, account_id);
    }

    //@GetMapping("/loan/{id}/passed")
    //@ApiOperation("查询-初筛通过")
    //public BaseResponse<List<JoinLoanActivityUserResponse>> getLoanActivityByIdA(
    //    @Valid @NotNull @PathVariable Long id) {
    //    return depositeActivityService.getPassedUsers(id);
    //}
    //
    //@GetMapping("/loan/{id}/unpassed")
    //@ApiOperation("查询-初筛不通过")
    //public BaseResponse<List<JoinLoanActivityUserResponse>> getLoanActivityByIdB(
    //    @Valid @NotNull @PathVariable Long id) {
    //    return depositeActivityService.getUnPassedUsers(id);
    //}

    //@GetMapping("/{activity_id}/passed")
    //@ApiOperation("查询-根据用户名字")
    //public BaseResponse<JoinLoanActivityUserResponse> ifUserPassed(@Valid @NotNull @PathVariable Long activity_id,
    //                                                               @NotNull @RequestParam String name) throws Exception {
    //    return depositeActivityService.getPassedUser(activity_id, name);
    //}
    //
    //@GetMapping("/{activity_id}/unpassed/{user_id}")
    //@ApiOperation("")
    //public BaseResponse<JoinLoanActivityUserResponse> ifUserUnPassed(@Valid @NotNull @PathVariable Long activity_id,
    //                                                                 @NotNull @RequestParam String name) throws Exception {
    //    return depositeActivityService.getUnpassedUser(activity_id, name);
    //}

}
