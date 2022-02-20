package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.dao.LoanActivityDao;
import com.moflowerlkh.decisionengine.dao.ShoppingGoodsDao;
import com.moflowerlkh.decisionengine.entity.LoanActivity;
import com.moflowerlkh.decisionengine.entity.LoanRule;
import com.moflowerlkh.decisionengine.entity.ShoppingGoods;
import com.moflowerlkh.decisionengine.enums.DateValue;
import com.moflowerlkh.decisionengine.service.LoanService;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.BaseResult;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.*;
import java.sql.Timestamp;
import java.util.*;

@RestController
@Api(tags = {"活动设置相关"})
@RequestMapping("/api/activity")
public class ActivityController {

    @Autowired
    LoanActivityDao loanActivityDao;
    @Autowired
    ShoppingGoodsDao shoppingGoodsDao;
    @Autowired
    LoanService loanService;

    @PostMapping("/loan/")
    @ApiOperation("新增活动")
    public BaseResponse<LoanActivity> setLoanActivity(@RequestBody @Valid SetLoanActivityRequest request) {
        LoanActivity loanActivity = request.toLoanActivity();
        loanActivityDao.save(loanActivity);
        return new BaseResponse<>(HttpStatus.CREATED, "新增成功", loanActivity);
    }

    @PutMapping("/loan/{id}")
    @ApiOperation("根据id修改活动信息")
    public BaseResponse<LoanActivity> editLoanActivity(@Valid @NotNull @PathVariable Long id, @RequestBody @Valid SetLoanActivityRequest request) {
        LoanActivity loanActivity = request.toLoanActivity();
        loanActivity.setId(id);
        loanActivityDao.saveAndFlush(loanActivity);
        return new BaseResponse<>(HttpStatus.CREATED, "修改成功", loanActivity);
    }

    @GetMapping("/loan/{id}")
    @ApiOperation("根据id查询活动信息")
    public BaseResponse<LoanActivity> getLoanActivityById(@Valid @NotNull @PathVariable Long id) {
        Optional<LoanActivity> _loanActivity = loanActivityDao.findById(id);
        LoanActivity loanActivity = _loanActivity.orElse(null);
        return new BaseResponse<>(HttpStatus.CREATED, "查询成功", loanActivity);
    }

    @DeleteMapping("/loan/{id}")
    @ApiOperation("根据id删除活动")
    public BaseResponse<LoanActivity> deleteLoanActivityById(@Valid @NotNull @PathVariable Long id) {
        loanActivityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.CREATED, "删除成功", null);
    }

    @GetMapping("/loan/{activity_id}/{user_id}/")
    @ApiOperation(value = "用户参加活动", notes = "某用户参加某活动")
    public BaseResponse<Boolean> joinLoanActivity(@Valid @NotNull @PathVariable Long activity_id, @Valid @NotNull @PathVariable Long user_id) throws Exception {
        BaseResult<Boolean> checkResult = loanService.checkUserInfo(activity_id, user_id);
        loanService.tryJoin(activity_id, user_id, checkResult.getResult());
        if (checkResult.getResult()) {
            return new BaseResponse<>(HttpStatus.CREATED, "初筛通过, 参加成功", true);
        } else {
            return new BaseResponse<>(HttpStatus.FORBIDDEN, "初筛不通过: " + checkResult.getMessage(), false);
        }
    }

}

@Data
class SetLoanActivityRuleRequest {
    //activity_guarantee	string	是否需要担保
    @NotNull(message = "是否需要担保不能为空")
    private Boolean activity_guarantee;
    //activity_pledge	string	是否需要抵押
    @NotNull(message = "是否需要抵押不能为空")
    private Boolean activity_pledge;
    //activity_ageUp	number	年龄上限
    @NotNull(message = "年龄上限不能为空")
    @PositiveOrZero(message = "年龄上限必须为0或正整数")
    private Integer activity_ageUp;
    //activity_ageFloor	number	年龄下限
    @PositiveOrZero(message = "年龄下限必须为0或正整数")
    @NotNull(message = "年龄下限不能为空")
    private Integer activity_ageFloor;
    //activity_checkwork	string	是否检查在职
    @NotNull(message = "是否检查在职不能为空")
    private Boolean activity_checkwork;
    //activity_checkDishonest	string	是否检查失信
    @NotNull(message = "是否检查失信人员不能为空")
    private Boolean activity_checkDishonest;
    //activity_checkOverdual	string	是否检查逾期
    @NotNull(message = "是否检查逾期不能为空")
    private Boolean activity_checkOverdual;
    //activity_checkNation	string	是否限制国内
    @NotNull(message = "是否限制国内")
    private Boolean activity_checkNation;

    public LoanRule toLoanRule() {
        LoanRule loanRule = new LoanRule();
        loanRule.setCheckGuarantee(activity_guarantee);
        loanRule.setCheckPledge(activity_pledge);
        loanRule.setMaxAge(activity_ageUp);
        loanRule.setMinAge(activity_ageFloor);
        loanRule.setCheckEmployment(activity_checkwork);
        loanRule.setCheckDishonest(activity_checkDishonest);
        loanRule.setCheckOverDual(activity_checkOverdual);
        loanRule.setCheckCountry(activity_checkNation);
        return loanRule;
    }
}

@Data
class SetLoanActivityRequest {
    //activity_id	string	活动序号
    //activity_name	string	活动名称
    @NotEmpty(message = "活动名称不能为空")
    private String activity_name;
    //activity_moneyLimit	number	借款额度
    @NotNull(message = "借款额度不能为空")
    @PositiveOrZero
    private Long activity_moneyLimit;

    // 分几期
    @NotEmpty(message = "借款期限不能为空")
    private String activity_timeLimit;

    // 还几年
    @NotEmpty(message = "还款期限不能为空")
    private String activity_replayTime;

    // 活动开始时间
    @DateValue(message = "活动开始时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_startTime;
    // 活动结束时间
    @DateValue(message = "活动结束时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_endTime;

    @NotNull(message = "年利率不能为空")
    @PositiveOrZero(message = "年利率不能为负数")
    private double activity_apr;
    // 活动规则
    @Valid
    @NotNull(message = "活动规则不能为空")
    private SetLoanActivityRuleRequest ruler;

    // 活动对应的商品
    @NotNull(message = "活动对应的商品id不能为空")
    private Long shoppinggoods_id;

    public LoanActivity toLoanActivity() {
        LoanActivity loanActivity = new LoanActivity();
        // 设置基本信息
        loanActivity.setName(activity_name);
        loanActivity.setMaxMoneyLimit(activity_moneyLimit);
        loanActivity.setTimeLimit(activity_timeLimit);
        loanActivity.setReplayLimit(activity_replayTime);
        loanActivity.setEndTime(Timestamp.valueOf(activity_endTime));
        loanActivity.setBeginTime(Timestamp.valueOf(activity_startTime));
        loanActivity.setApr(activity_apr);

        // 添加规则
        LoanRule loanRule = ruler.toLoanRule();
        loanActivity.setRule(loanRule);

        // 添加商品
        ShoppingGoods shoppingGoods = new ShoppingGoods();
        shoppingGoods.setId(shoppinggoods_id);
        loanActivity.setShoppingGoods(shoppingGoods);
        return loanActivity;
    }
}


