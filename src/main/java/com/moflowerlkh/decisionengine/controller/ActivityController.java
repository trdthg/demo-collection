package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.domain.entities.ShoppingGoods;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.dao.LoanActivityDao;
import com.moflowerlkh.decisionengine.domain.dao.ShoppingGoodsDao;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;
import com.moflowerlkh.decisionengine.vo.enums.DateValue;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.*;
import java.sql.Timestamp;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@Api(tags = { "活动设置相关" })
@RequestMapping("/api/activity")
public class ActivityController {

    @Autowired
    LoanActivityDao loanActivityDao;
    @Autowired
    ShoppingGoodsDao shoppingGoodsDao;

    @PostMapping("/loan/")
    @ApiOperation(value = "新增活动", notes = "")
    public BaseResponse<LoanActivityResponse> setLoanActivity(@RequestBody @Valid SetLoanActivityRequest request) {
        LoanActivity loanActivity = request.toLoanActivity();
        loanActivityDao.save(loanActivity);
        return new BaseResponse<>(HttpStatus.CREATED, "新增成功", LoanActivityResponse.fromLoanActivity(loanActivity));
    }

    @PutMapping("/loan/{id}")
    @ApiOperation(value = "根据id修改活动信息-全部", notes = "需要传完整，传来的信息会直接全部覆盖掉原来的")
    public BaseResponse<LoanActivityResponse> editLoanActivityPut(@Valid @NotNull @PathVariable Long id,
            @RequestBody @Valid SetLoanActivityRequest request) {
        LoanActivity loanActivity = request.toLoanActivity();
        loanActivity.setId(id);
        loanActivityDao.saveAndFlush(loanActivity);
        return new BaseResponse<>(HttpStatus.OK, "修改成功", LoanActivityResponse.fromLoanActivity(loanActivity));
    }

    @PatchMapping("/loan/{id}")
    @ApiOperation(value = "根据id修改活动信息-部分 todo!", notes = "需要修改那些字段，就只用传递那些字段")
    public BaseResponse<SetLoanActivityRequest> editLoanActivityPatch(@Valid @NotNull @PathVariable Long id,
            @RequestBody SetLoanActivityRequest request) {
        // LoanActivity loanActivity = request.toLoanActivity();
        // loanActivity.setId(id);
        // loanActivityDao.saveAndFlush(loanActivity);
        return new BaseResponse<>(HttpStatus.OK, "修改成功", request);
    }

    @GetMapping("/loan")
    @ApiOperation(value = "查询活动列表-不带初筛信息", notes = "只有一些活动的基本信息")
    public BaseResponse<PageResult<List<LoanActivitySimpleResponse>>> getLoanActivityByIdSimple(
            @RequestParam Integer page_num, @RequestParam Integer page_limit) {
        Page<LoanActivity> loanActivities = loanActivityDao
                .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")));
        Integer pages = loanActivities.getTotalPages();
        List<LoanActivitySimpleResponse> res = loanActivities.stream().map(LoanActivitySimpleResponse::fromLoanActivity)
                .collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    @GetMapping("/loan/full")
    @ApiOperation(value = "查询活动列表-带有初筛信息", notes = "除了活动的基本信息之外，还包含初筛的通过者，未通过者信息")
    public BaseResponse<PageResult<List<LoanActivityResponse>>> getLoanActivityByIdFull(@RequestParam Integer page_num,
            @RequestParam Integer page_limit) {
        Page<LoanActivity> loanActivities = loanActivityDao
                .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")));
        Integer pages = loanActivities.getTotalPages();
        List<LoanActivityResponse> res = loanActivities.stream().map(LoanActivityResponse::fromLoanActivity)
                .collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    @GetMapping("/loan/{id}")
    @ApiOperation(value = "根据id查询活动信息-简略", notes = "不带有活动的参加信息")
    public BaseResponse<LoanActivitySimpleResponse> getLoanActivityByIdSimple(@Valid @NotNull @PathVariable Long id) {
        Optional<LoanActivity> _loanActivity = loanActivityDao.findById(id);
        LoanActivity loanActivity = _loanActivity.orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", LoanActivitySimpleResponse.fromLoanActivity(loanActivity));
    }

    @GetMapping("/loan/{id}/full")
    @ApiOperation(value = "根据id查询活动信息-完整", notes = "带有活动的参加信息")
    public BaseResponse<LoanActivityResponse> getLoanActivityByIdFull(@Valid @NotNull @PathVariable Long id) {
        Optional<LoanActivity> _loanActivity = loanActivityDao.findById(id);
        LoanActivity loanActivity = _loanActivity.orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", LoanActivityResponse.fromLoanActivity(loanActivity));
    }

    @GetMapping("/loan/{id}/passed")
    @ApiOperation("查询活动通过者信息")
    public BaseResponse<List<JoinLoanActivityUserResponse>> getLoanActivityByIdA(
            @Valid @NotNull @PathVariable Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        List<JoinLoanActivityUserResponse> res = loanActivity.getUserLoanActivities().stream()
                .filter(x -> x.getIsPassed()).map(x -> x.getUser())
                .map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);

    }

    @GetMapping("/loan/{id}/unpassed")
    @ApiOperation("查询活动不通过者信息")
    public BaseResponse<List<JoinLoanActivityUserResponse>> getLoanActivityByIdB(
            @Valid @NotNull @PathVariable Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        List<JoinLoanActivityUserResponse> res = loanActivity.getUserLoanActivities().stream()
                .filter(x -> !x.getIsPassed()).map(x -> x.getUser())
                .map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }

    @GetMapping("/{activity_id}/passed")
    @ApiOperation("查看通过某活动筛选的某用户信息")
    public BaseResponse<JoinLoanActivityUserResponse> ifUserPassed(@Valid @NotNull @PathVariable Long activity_id,
            @NotNull @RequestParam String name) throws Exception {
        LoanActivity activity = loanActivityDao.findById(activity_id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        List<User> users = activity.getUserLoanActivities().stream().filter(x -> {
            return Objects.equals(x.getUser().getName(), name);
        }).map(x -> x.getUser()).collect(Collectors.toList());
        if (users.isEmpty()) {
            throw new DataRetrievalFailureException("该用户没有参加该活动或者未通过筛选");
        }
        return new BaseResponse<>(HttpStatus.OK, "查询成功", JoinLoanActivityUserResponse.fromUser(users.get(0)));
    }

    @GetMapping("/{activity_id}/unpassed/{user_id}")
    @ApiOperation("查看未通过某活动筛选的某用户信息")
    public BaseResponse<JoinLoanActivityUserResponse> ifUserUnPassed(@Valid @NotNull @PathVariable Long user_id,
            @Valid @NotNull @PathVariable Long activity_id) throws Exception {
        LoanActivity activity = loanActivityDao.findById(activity_id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        List<User> users = activity.getUserLoanActivities().stream()
                .filter(x -> !x.getIsPassed() && Objects.equals(x.getUser().getId(), user_id)).map(x -> x.getUser())
                .collect(Collectors.toList());
        if (users.isEmpty()) {
            throw new DataRetrievalFailureException("该用户没有参加该活动或者已经通过筛选");
        }
        return new BaseResponse<>(HttpStatus.OK, "查询成功", JoinLoanActivityUserResponse.fromUser(users.get(0)));
    }

    @DeleteMapping("/loan/{id}")
    @ApiOperation("根据id删除活动")
    public BaseResponse<Boolean> deleteLoanActivityById(@Valid @NotNull @PathVariable Long id) {
        loanActivityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", true);
    }
}

@Data
class JoinLoanActivityUserResponse {
    private Long user_id;
    private String user_name;
    private String user_gender;
    private String user_IDnumber;
    private String user_nation;
    private Integer user_age;
    private Long user_overdual;
    private String user_employment;
    private Boolean user_dishonest;

    public static JoinLoanActivityUserResponse fromUser(User user) {
        JoinLoanActivityUserResponse response = new JoinLoanActivityUserResponse();
        response.setUser_id(user.getId());
        response.setUser_name(user.getName());
        response.setUser_gender(user.getGender().name());
        response.setUser_IDnumber(user.getIDNumber());
        response.setUser_nation(user.getCountry());
        response.setUser_age(user.getAge());
        response.setUser_overdual(user.getOverDual());
        response.setUser_employment(user.getEmployment().name());
        response.setUser_dishonest(user.getDishonest());
        return response;
    }

    public static List<JoinLoanActivityUserResponse> fromUser(List<User> users) {
        return users.stream().map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());
    }
}

@Data
class LoanActivitySimpleResponse {
    private Long activity_id;
    // activity_id string 活动序号
    private String activity_name;
    // activity_name string 活动名称
    private Double activity_moneyLimit;
    // activity_moneyLimit number 借款额度
    private String activity_timeLimit;
    // activity_timeLimit string 借款期限
    private Integer activity_replayTime;
    // activity_replayTime string 还款期限
    private Double activity_apr;
    // activity_apr string 年利率
    private SetLoanActivityRuleRequest rule;
    // activity_dateRate bool 是否当日起息
    // activity_dawa bool 是否随存随取
    // activity_sum number 产品总数量
    // activity_startTime date 产品秒杀开始时间
    // activity_endTime date 产品秒杀结束时间
    private Long activity_totalQuantity;
    private Long activity_totalAmount;
    private double activity_initMoney;
    // activity_sum number 产品总数量
    private String activity_startTime;
    // activity_startTime date 产品秒杀开始时间
    private String activity_endTime;
    // activity_endTime date 产品秒杀结束时间

    public static LoanActivitySimpleResponse fromLoanActivity(LoanActivity loanActivity) {
        LoanActivitySimpleResponse response = new LoanActivitySimpleResponse();
        response.setActivity_id(loanActivity.getId());
        response.setActivity_name(loanActivity.getName());
        response.setActivity_moneyLimit(loanActivity.getMaxMoneyLimit());
        response.setActivity_timeLimit(loanActivity.getTimeLimit());
        response.setActivity_replayTime(loanActivity.getReplayLimit());
        response.setActivity_apr(loanActivity.getApr());

        response.setActivity_totalQuantity(loanActivity.getShoppingGoods().getGoodsAmount());
        response.setActivity_totalAmount(loanActivity.getMoneyTotal());
        response.setActivity_initMoney(loanActivity.getMinMoneyLimit());

        String s = loanActivity.getBeginTime().toString();
        response.setActivity_startTime(s.substring(0, s.indexOf('.')));
        s = loanActivity.getEndTime().toString();
        response.setActivity_endTime(s.substring(0, s.indexOf('.')));

        response.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanActivity.getRule()));

        return response;
    }
}

@Data
class LoanActivityResponse {
    private Long activity_id;
    // activity_id string 活动序号
    private String activity_name;
    // activity_name string 活动名称
    private Double activity_moneyLimit;
    // activity_moneyLimit number 借款额度
    private String activity_timeLimit;
    // activity_timeLimit string 借款期限
    private Integer activity_replayTime;
    // activity_replayTime string 还款期限
    private Double activity_apr;
    // activity_apr string 年利率
    private SetLoanActivityRuleRequest rule;
    // activity_dateRate bool 是否当日起息
    // activity_dawa bool 是否随存随取
    // activity_sum number 产品总数量
    // activity_startTime date 产品秒杀开始时间
    // activity_endTime date 产品秒杀结束时间
    private Long activity_totalQuantity;
    private Long activity_totalAmount;
    private double activity_initMoney;
    // activity_sum number 产品总数量
    private String activity_startTime;
    // activity_startTime date 产品秒杀开始时间
    private String activity_endTime;
    // activity_endTime date 产品秒杀结束时间

    private List<JoinLoanActivityUserResponse> passed_users;
    private List<JoinLoanActivityUserResponse> unPassed_users;

    public static LoanActivityResponse fromLoanActivity(LoanActivity loanActivity) {
        LoanActivityResponse response = new LoanActivityResponse();
        response.setActivity_id(loanActivity.getId());
        response.setActivity_name(loanActivity.getName());
        response.setActivity_moneyLimit(loanActivity.getMaxMoneyLimit());
        response.setActivity_timeLimit(loanActivity.getTimeLimit());
        response.setActivity_replayTime(loanActivity.getReplayLimit());
        response.setActivity_apr(loanActivity.getApr());

        response.setActivity_totalQuantity(loanActivity.getShoppingGoods().getGoodsAmount());
        response.setActivity_totalAmount(loanActivity.getMoneyTotal());
        response.setActivity_initMoney(loanActivity.getMinMoneyLimit());

        String s = loanActivity.getBeginTime().toString();
        response.setActivity_startTime(s.substring(0, s.indexOf('.')));
        s = loanActivity.getEndTime().toString();
        response.setActivity_endTime(s.substring(0, s.indexOf('.')));

        response.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanActivity.getRule()));
        // return
        // users.stream().map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());

        response.setPassed_users(JoinLoanActivityUserResponse.fromUser(new ArrayList<>(
                loanActivity.getUserLoanActivities().stream()
                        .filter(x -> x.getIsPassed())
                        .map(x -> x.getUser())
                        .collect(Collectors.toList()))));
        response.setUnPassed_users(
                JoinLoanActivityUserResponse.fromUser(new ArrayList<>(
                        loanActivity.getUserLoanActivities().stream()
                                .filter(x -> !x.getIsPassed())
                                .map(x -> x.getUser())
                                .collect(Collectors.toList()))));
        return response;
    }
}

@Data
class JoinLoanActivityResponse {
    private List<JoinLoanActivityUserResponse> passed_users;
    private List<JoinLoanActivityUserResponse> unPassed_users;

    public static JoinLoanActivityResponse fromLoanActivity(LoanActivity loanActivity) {
        JoinLoanActivityResponse response = new JoinLoanActivityResponse();
        response.setPassed_users(
                JoinLoanActivityUserResponse.fromUser(new ArrayList<>(loanActivity.getUserLoanActivities().stream()
                        .filter(x -> x.getIsPassed())
                        .map(x -> x.getUser())
                        .collect(Collectors.toList()))));
        response.setUnPassed_users(
                JoinLoanActivityUserResponse.fromUser(new ArrayList<>(loanActivity.getUserLoanActivities().stream()
                        .filter(x -> !x.getIsPassed())
                        .map(x -> x.getUser())
                        .collect(Collectors.toList()))));
        return response;
    }
}

@Data
class SetLoanActivityRuleRequest {
    // activity_guarantee string 是否需要担保
    @NotNull(message = "是否需要担保不能为空")
    private Boolean activity_guarantee;
    // activity_pledge string 是否需要抵押
    @NotNull(message = "是否需要抵押不能为空")
    private Boolean activity_pledge;
    // activity_ageUp number 年龄上限
    @NotNull(message = "年龄上限不能为空")
    @PositiveOrZero(message = "年龄上限必须为0或正整数")
    private Integer activity_ageUp;
    // activity_ageFloor number 年龄下限
    @PositiveOrZero(message = "年龄下限必须为0或正整数")
    @NotNull(message = "年龄下限不能为空")
    private Integer activity_ageFloor;
    // activity_checkwork string 是否检查在职
    @NotNull(message = "是否检查在职不能为空")
    private Boolean activity_checkwork;
    // activity_checkDishonest string 是否检查失信
    @NotNull(message = "是否检查失信人员不能为空")
    private Boolean activity_checkDishonest;
    // activity_checkOverdual string 是否检查逾期
    @NotNull(message = "是否检查逾期不能为空")
    private Boolean activity_checkOverdual;
    // activity_checkNation string 是否限制国内
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

    public static SetLoanActivityRuleRequest fromLoanRule(LoanRule loanRule) {
        SetLoanActivityRuleRequest res = new SetLoanActivityRuleRequest();
        res.setActivity_guarantee(loanRule.getCheckGuarantee());
        res.setActivity_pledge(loanRule.getCheckPledge());
        res.setActivity_ageUp(loanRule.getMaxAge());
        res.setActivity_ageFloor(loanRule.getMinAge());
        res.setActivity_checkwork(loanRule.getCheckEmployment());
        res.setActivity_checkDishonest(loanRule.getCheckDishonest());
        res.setActivity_checkOverdual(loanRule.getCheckOverDual());
        res.setActivity_checkNation(loanRule.getCheckCountry());
        return res;
    }
}

@Data
class SetLoanActivityRequest {
    // activity_id string 活动序号
    // activity_name string 活动名称
    @NotEmpty(message = "活动名称不能为空")
    private String activity_name;
    // activity_moneyLimit number 借款额度
    @NotNull(message = "借款额度不能为空")
    @PositiveOrZero(message = "借款额度不能为负")
    private Long activity_moneyLimit;

    // 分几期
    @NotEmpty(message = "借款期限不能为空")
    private String activity_timeLimit;

    // 还几年
    @NotNull(message = "还款期限不能为空")
    @PositiveOrZero(message = "还款期限不能为负")
    private Integer activity_replayTime;

    // 活动开始时间
    @DateValue(message = "活动开始时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_startTime;
    // 活动结束时间
    @DateValue(message = "活动结束时间格式必须为: `yyyy-mm-dd hh:mm:ss[.fffffffff]`")
    private String activity_endTime;

    @NotNull(message = "年利率不能为空")
    @PositiveOrZero(message = "年利率不能为负数")
    private double activity_apr;

    @NotNull(message = "产品总数量不能为空")
    @PositiveOrZero(message = "产品总数量必须为0或正整数")
    private Long activity_totalQuantity;
    @NotNull(message = "产品总金额不能为空")
    @PositiveOrZero(message = "产品总金额必须为0或正整数")
    private Long activity_totalAmount;
    @NotNull(message = "起贷金额不能为空")
    @PositiveOrZero(message = "起贷金额必须为>=0")
    private double activity_initMoney;

    // 活动规则
    @Valid
    @NotNull(message = "活动规则不能为空")
    private SetLoanActivityRuleRequest rule;

    // 活动对应的商品
    // @NotNull(message = "活动对应的商品id不能为空")
    // private Long shoppinggoods_id;

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

        ShoppingGoods shoppingGoods = new ShoppingGoods();
        shoppingGoods.setName(loanActivity.getName());
        shoppingGoods.setGoodsAmount(activity_totalQuantity);

        loanActivity.setShoppingGoods(shoppingGoods);
        loanActivity.setMoneyTotal(activity_totalAmount);
        loanActivity.setMinMoneyLimit(activity_initMoney);

        // 添加规则
        LoanRule loanRule = rule.toLoanRule();
        loanActivity.setRule(loanRule);

        return loanActivity;
    }
}
