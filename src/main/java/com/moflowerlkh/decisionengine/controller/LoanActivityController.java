package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.component.AccessLimiter;
import com.moflowerlkh.decisionengine.component.RequestLimiter;
import com.moflowerlkh.decisionengine.service.*;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.*;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

@RestController
@Api(tags = {"Loan 贷款活动"})
@RequestMapping("/api/loan")
public class LoanActivityController {

    @Autowired
    LoanActivityService loanActivityService;

    @PostMapping("/")
    @ApiOperation(value = "新增", notes = "创建一个新活动，同时会创建一个新商品，商品购买后的所得金额会进入创建者的账户")
    public BaseResponse<LoanActivitySimpleResponseDTO> setLoanActivity(@RequestBody @Valid SetLoanActivityRequestDTO request) {
        return loanActivityService.setLoanActivity(request);
    }

    @PutMapping("/{id}")
    @ApiOperation(value = "修改", notes = "需要传完整，传来的信息会直接全部覆盖掉原来的")
    public BaseResponse<LoanActivitySimpleResponseDTO> editLoanActivityPut(@Valid @NotNull @PathVariable Long id,
                                                                     @RequestBody @Valid SetLoanActivityRequestDTO request) {
        return loanActivityService.changeActivityInfo(id, request);
    }

    //@PatchMapping("/loan/{id}")
    //@ApiOperation(value = "修改-部分 todo!", notes = "需要修改那些字段，就只用传递那些字段")
    //public BaseResponse<SetLoanActivityRequest> editLoanActivityPatch(@Valid @NotNull @PathVariable Long id,
    //                                                                  @RequestBody SetLoanActivityRequest request) {
    //    return new BaseResponse<>(HttpStatus.OK, "修改成功", request);
    //}

    @GetMapping("/")
    @ApiOperation(value = "分页查询-无初筛结果", notes = "只有一些活动的基本信息")
    public BaseResponse<PageResult<List<LoanActivitySimpleResponseDTO>>> getLoanActivityByIdSimple(
            @RequestParam Integer page_num, @RequestParam Integer page_limit) {
        return loanActivityService.findAllActivityPartial(page_num, page_limit);
    }

    //@GetMapping("/full")
    //@ApiOperation(value = "分页查询-有初筛结果", notes = "除了活动的基本信息之外，还包含初筛的通过者，未通过者信息")
    //public BaseResponse<PageResult<List<LoanActivityResponseDTO>>> getLoanActivityByIdFull(@RequestParam Integer page_num,
    //                                                                                       @RequestParam Integer page_limit) {
    //    return loanActivityService.findAllActivity(page_num, page_limit);
    //}

    @GetMapping("/{id}")
    @ApiOperation(value = "查询-无初筛结果", notes = "不带有活动的参加信息")
    public BaseResponse<LoanActivitySimpleResponseDTO> getLoanActivityByIdSimple(@Valid @NotNull @PathVariable Long id) {
        return loanActivityService.findByIdPartial(id);
    }

    //@GetMapping("/{id}/full")
    //@ApiOperation(value = "查询-有初筛结果", notes = "带有活动的参加信息")
    //public BaseResponse<LoanActivityResponseDTO> getLoanActivityByIdFull(@Valid @NotNull @PathVariable Long id) {
    //    return loanActivityService.findById(id);
    //}

    @AccessLimiter(key = "loan_join", limit = 10, timeout = 2)
    @RequestLimiter(QPS = 300, timeout = 1)
    @GetMapping("/join")
    @ApiOperation(value = "参加活动", notes = "某用户参加某活动")
    public BaseResponse<TryJoinResponseDTO> joinLoanActivity(@Valid @NotNull Long activity_id,
                                                             @Valid @NotNull Long user_id,
                                                             @Valid @NotNull String account_id)
        throws Exception {
        return loanActivityService.tryJoin(activity_id, user_id, account_id);
    }

    @GetMapping("/check")
    @ApiOperation(value = "初筛", notes = "参加活动前需要初筛")
    public BaseResponse<Boolean> check(@Valid @NotNull Long activity_id,
                                       @Valid @NotNull Long user_id)
        throws Exception {
        return loanActivityService.check(activity_id, user_id);
    }

    @DeleteMapping("/{id}")
    @ApiOperation("删除")
    public BaseResponse<Boolean> deleteLoanActivityById(@Valid @NotNull @PathVariable Long id) {
        return loanActivityService.deleteActivity(id);
    }

    //@ApiOperation("获取图片验证码")
    //@GetMapping("/getCaptchaBase64")
    //@ResponseBody
    //public BaseResponse<String> getCaptchaBase64() {
    //    return loanActivityService.generateCaptchaBase64();
    //}
}