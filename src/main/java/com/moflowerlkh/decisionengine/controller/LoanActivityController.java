package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.service.*;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponseDTO;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.LoanActivityResponseDTO;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.LoanActivitySimpleResponseDTO;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.SetLoanActivityRequestDTO;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.*;
import java.util.*;

@RestController
@Api(tags = {"Loan 贷款活动"})
@RequestMapping("/api/activity")
public class LoanActivityController {

    @Autowired
    LoanActivityService loanActivityService;

    @PostMapping("/loan/")
    @ApiOperation(value = "新增", notes = "创建一个新活动，同时会创建一个新商品，商品购买后的所得金额会进入创建者的账户")
    public BaseResponse<LoanActivityResponseDTO> setLoanActivity(@RequestBody @Valid SetLoanActivityRequestDTO request) {
        return loanActivityService.setLoanActivity(request);
    }

    @PutMapping("/loan/{id}")
    @ApiOperation(value = "修改-全部", notes = "需要传完整，传来的信息会直接全部覆盖掉原来的")
    public BaseResponse<LoanActivityResponseDTO> editLoanActivityPut(@Valid @NotNull @PathVariable Long id,
                                                                     @RequestBody @Valid SetLoanActivityRequestDTO request) {
        return loanActivityService.changeActivityInfo(id, request);
    }

    //@PatchMapping("/loan/{id}")
    //@ApiOperation(value = "修改-部分 todo!", notes = "需要修改那些字段，就只用传递那些字段")
    //public BaseResponse<SetLoanActivityRequest> editLoanActivityPatch(@Valid @NotNull @PathVariable Long id,
    //                                                                  @RequestBody SetLoanActivityRequest request) {
    //    return new BaseResponse<>(HttpStatus.OK, "修改成功", request);
    //}

    @GetMapping("/loan")
    @ApiOperation(value = "分页查询-无初筛结果", notes = "只有一些活动的基本信息")
    public BaseResponse<PageResult<List<LoanActivitySimpleResponseDTO>>> getLoanActivityByIdSimple(
            @RequestParam Integer page_num, @RequestParam Integer page_limit) {
        return loanActivityService.findAllActivityPartial(page_num, page_limit);
    }

    @GetMapping("/loan/full")
    @ApiOperation(value = "分页查询-有初筛结果", notes = "除了活动的基本信息之外，还包含初筛的通过者，未通过者信息")
    public BaseResponse<PageResult<List<LoanActivityResponseDTO>>> getLoanActivityByIdFull(@RequestParam Integer page_num,
                                                                                           @RequestParam Integer page_limit) {
        return loanActivityService.findAllActivity(page_num, page_limit);
    }

    @GetMapping("/loan/{id}")
    @ApiOperation(value = "查询-无初筛结果", notes = "不带有活动的参加信息")
    public BaseResponse<LoanActivitySimpleResponseDTO> getLoanActivityByIdSimple(@Valid @NotNull @PathVariable Long id) {
        return loanActivityService.findByIdPartial(id);
    }

    @GetMapping("/loan/{id}/full")
    @ApiOperation(value = "查询-有初筛结果", notes = "带有活动的参加信息")
    public BaseResponse<LoanActivityResponseDTO> getLoanActivityByIdFull(@Valid @NotNull @PathVariable Long id) {
        return loanActivityService.findById(id);
    }

    @GetMapping("/loan/{id}/passed")
    @ApiOperation("查询-初筛通过")
    public BaseResponse<List<JoinLoanActivityUserResponseDTO>> getLoanActivityByIdA(
            @Valid @NotNull @PathVariable Long id) {
        return loanActivityService.getPassedUsers(id);

    }

    @GetMapping("/loan/{id}/unpassed")
    @ApiOperation("查询-初筛不通过")
    public BaseResponse<List<JoinLoanActivityUserResponseDTO>> getLoanActivityByIdB(
            @Valid @NotNull @PathVariable Long id) {
        return loanActivityService.getUnPassedUsers(id);
    }

    @GetMapping("/{activity_id}/passed")
    @ApiOperation("查询通过-根据用户名字")
    public BaseResponse<JoinLoanActivityUserResponseDTO> ifUserPassed(@Valid @NotNull @PathVariable Long activity_id,
                                                                      @NotNull @RequestParam String name) throws Exception {
        return loanActivityService.getPassedUser(activity_id, name);
    }

    @GetMapping("/{activity_id}/unpassed")
    @ApiOperation("查询未通过-根据用户名字")
    public BaseResponse<JoinLoanActivityUserResponseDTO> ifUserUnPassed(@Valid @NotNull @PathVariable Long activity_id,
                                                                        @NotNull @RequestParam String name) throws Exception {
        return loanActivityService.getUnpassedUser(activity_id, name);
    }

    @DeleteMapping("/loan/{id}")
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