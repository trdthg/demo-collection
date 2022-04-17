package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.*;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.schedule.ActivityTask;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.*;
import com.moflowerlkh.decisionengine.util.CodeResult;
import com.moflowerlkh.decisionengine.util.MD5;
import com.moflowerlkh.decisionengine.util.ValidateCode;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
//import io.micrometer.core.annotation.Counted;
//import io.micrometer.core.annotation.Timed;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import javax.validation.Valid;
import java.sql.Timestamp;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static com.moflowerlkh.decisionengine.service.ActivityService.LOAN_ACTIVITY_TYPE;

@Service
public class LoanActivityService {
    @Autowired
    ActivityDao activityDao;
    @Autowired
    GoodsDao goodsDao;
    @Autowired
    LoanRuleDao loanRuleDao;
    @Autowired
    UserDao userDao;
    @Autowired
    UserActivityDao userActivityDao;
    @Autowired
    RedisService redisService;
    @Autowired
    AuthenticationManager authenticationManager;
    @Autowired
    StringRedisTemplate stringRedisTemplate;
    @Autowired
    BankAccountDao bankAccountDao;

    public static final String ScheduleKey = "SCHEDULE_KEY";
    public static final String ACTIVITY_TO_GOODS_KEY = "ACTIVITY_TO_GOODS_KEY";
    public static final String AUTH_SALT = "bc30a3c8-b96b-49d2-bb9f-1c28f9408eb3";
    public static final String USER_SEND_REQUEST_TIME_KEY = "USER_SEND_REQUEST_TIME_KEY";
    public static final String USER_CHECK_LOAN_CACHE = "USER_CHECK_LOAN_CACHE";
    public static final String USER_MD5_CACHE = "USER_MD5_CACHE";

    public BaseResponse<LoanActivitySimpleResponseDTO> setLoanActivity(
            @RequestBody @Valid SetLoanActivityRequestDTO request) {

        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
                .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        User user = userDao.getById(loginUser.getId());
        List<BankAccount> accounts = bankAccountDao.findByUserID(user.getId());
        if (accounts.isEmpty()) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "您需要有至少一张银行卡", null);
        }

        Activity activity = new Activity();
        activity.setName(request.getActivity_name());
        activity.setEndTime(Timestamp.valueOf(request.getActivity_endTime()));
        activity.setBeginTime(Timestamp.valueOf(request.getActivity_startTime()));

        Goods goods = new Goods();
        goods.setStartTime(activity.getBeginTime());
        goods.setBankAccountSN(accounts.get(0).getBankAccountSN());
        goods.setPrice(request.getActivity_perPrice() * -1L);
        goods.setOneMaxAmount(request.getActivity_oneMaxAmount());
        goods.setGoodsAmount(request.getActivity_totalQuantity() * request.getActivity_oneMaxAmount());
        goodsDao.save(goods);

        LoanRule loanRule = request.getRule().toLoanRule(request.getActivity_initMoney(),
                request.getActivity_moneyLimit(), request.getActivity_apr(), request.getActivity_timeLimit(),
                request.getActivity_replayTime(), request.getActivity_totalQuantity());
        loanRuleDao.save(loanRule);

        activity.setGoodsId(goods.getId());
        activity.setRuleId(loanRule.getId());
        // 新建活动
        activity.setType(LOAN_ACTIVITY_TYPE);
        activityDao.save(activity);

        // 保存开始时间
        stringRedisTemplate.opsForValue().set(ScheduleKey + "." + activity.getId(),
                String.valueOf(new Date().getTime()));

        LoanActivitySimpleResponseDTO res = LoanActivitySimpleResponseDTO.fromLoanActivity(activity, loanRule, goods);
        res.setRule(SetLoanActivityRuleRequestDTO.fromLoanRule(loanRule));
        return new BaseResponse<>(HttpStatus.OK, "新增成功", res);
    }

    public BaseResponse<LoanActivitySimpleResponseDTO> changeActivityInfo(Long id, SetLoanActivityRequestDTO request) {

        Activity activity = activityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动失败"));
        if (!activity.getType().equals(LOAN_ACTIVITY_TYPE)) {
            throw new DataRetrievalFailureException("查询活动失败");
        }
        LoanRule loanRule = loanRuleDao.findById(activity.getRuleId())
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动规则失败"));
        Goods goods = goodsDao.findById(activity.getGoodsId())
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动对应的商品失败"));

        activity.setName(request.getActivity_name());
        activity.setEndTime(Timestamp.valueOf(request.getActivity_endTime()));
        activity.setBeginTime(Timestamp.valueOf(request.getActivity_startTime()));

        activityDao.saveAndFlush(activity);
        goods.setPrice(request.getActivity_perPrice() * -1L);
        goods.setStartTime(Timestamp.valueOf(request.getActivity_startTime()));
        goods.setOneMaxAmount(request.getActivity_oneMaxAmount());
        goods.setGoodsAmount(request.getActivity_totalQuantity() * request.getActivity_oneMaxAmount());
        goodsDao.saveAndFlush(goods);

        LoanRule loanRule1 = request.getRule().toLoanRule(request.getActivity_initMoney(),
                request.getActivity_moneyLimit(), request.getActivity_apr(), request.getActivity_timeLimit(),
                request.getActivity_replayTime(), request.getActivity_totalQuantity());
        loanRule1.setId(loanRule.getId());
        loanRuleDao.saveAndFlush(loanRule1);
        return new BaseResponse<>(HttpStatus.OK, "修改成功",
                LoanActivitySimpleResponseDTO.fromLoanActivity(activity, loanRule, goods));
    }

    public BaseResponse<PageResult<List<LoanActivitySimpleResponseDTO>>> findAllActivityPartial(Integer page_num,
            Integer page_limit) {
        Page<Activity> loanActivities = activityDao
                .findAllByType(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")),
                        LOAN_ACTIVITY_TYPE);
        Integer pages = loanActivities.getTotalPages();
        List<LoanActivitySimpleResponseDTO> res = loanActivities.stream().map(loanActivity -> {
            LoanRule rule = loanRuleDao.findById(loanActivity.getRuleId())
                    .orElseThrow(() -> new DataRetrievalFailureException("没有查询到活动规则"));
            Goods goods = goodsDao.findById(loanActivity.getGoodsId())
                    .orElseThrow(() -> new DataRetrievalFailureException("没有查询到活动商品"));
            LoanActivitySimpleResponseDTO response = LoanActivitySimpleResponseDTO.fromLoanActivity(loanActivity, rule,
                    goods);
            response.setRule(SetLoanActivityRuleRequestDTO.fromLoanRule(rule));
            return response;
        })
                .collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<LoanActivitySimpleResponseDTO> findByIdPartial(Long id) {
        Activity loanActivity = activityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        if (!loanActivity.getType().equals(LOAN_ACTIVITY_TYPE)) {
            throw new DataRetrievalFailureException("查询活动失败");
        }
        LoanRule rule = loanRuleDao.findById(loanActivity.getRuleId())
                .orElseThrow(() -> new DataRetrievalFailureException("查询该活动规则失败"));
        Goods goods = goodsDao.findById(loanActivity.getGoodsId())
                .orElseThrow(() -> new DataRetrievalFailureException("活动没有对应的商品"));
        LoanActivitySimpleResponseDTO response = LoanActivitySimpleResponseDTO.fromLoanActivity(loanActivity, rule,
                goods);
        response.setRule(SetLoanActivityRuleRequestDTO.fromLoanRule(rule));

        return new BaseResponse<>(HttpStatus.OK, "查询成功", response);
    }

    // public BaseResponse<PageResult<List<LoanActivityResponseDTO>>>
    // findAllActivity(Integer page_num, Integer page_limit) {
    // Page<Activity> loanActivities = activityDao
    // .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC,
    // "id")));
    // Integer pages = loanActivities.getTotalPages();
    // List<LoanActivityResponseDTO> res =
    // fetchLoanActivityResponses(loanActivities.toList());
    // return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res,
    // pages));
    // }

    // public List<LoanActivityResponseDTO>
    // fetchLoanActivityResponses(List<Activity> loanActivities) {
    // List<LoanActivityResponseDTO> res = loanActivities.stream().filter(x ->
    // x.getType().equals(1)).map(loanActivity -> {
    // LoanRule rule = loanRuleDao.findById(loanActivity.getRuleId()).orElseThrow(()
    // -> new DataRetrievalFailureException("查询该活动规则失败"));
    // Goods goods = goodsDao.findById(loanActivity.getGoodsId()).orElseThrow(() ->
    // new DataRetrievalFailureException("活动没有对应的商品"));
    // LoanActivityResponseDTO response =
    // LoanActivityResponseDTO.fromLoanActivity(loanActivity, rule, goods);
    //
    // response.setRule(SetLoanActivityRuleRequestDTO.fromLoanRule(rule));
    //
    // List<UserActivity> userLoanActivities =
    // userActivityDao.findByActivityId(loanActivity.getId());
    // response.setPassed_users(userLoanActivities.stream().filter(UserActivity::getIsPassed).map(x
    // -> {
    // User user = userDao.getById(x.getUserId());
    // return JoinLoanActivityUserResponseDTO.fromUser(user);
    // }).collect(Collectors.toList()));
    // response.setUnPassed_users(userLoanActivities.stream().filter(x ->
    // !x.getIsPassed()).map(x -> {
    // User user = userDao.getById(x.getUserId());
    // return JoinLoanActivityUserResponseDTO.fromUser(user);
    // }).collect(Collectors.toList()));
    //
    // response.setPerPrice(goods.getPrice());
    // response.setOneMaxAmount(goods.getOneMaxAmount());
    // return response;
    // }).collect(Collectors.toList());
    // return res;
    // }

    // public BaseResponse<LoanActivityResponseDTO> findById(Long id) {
    // Activity loanActivity = activityDao.findById(id)
    // .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
    // if (!loanActivity.getType().equals(LOAN_ACTIVITY_TYPE)) {
    // throw new DataRetrievalFailureException("没有该活动");
    // }
    // List<LoanActivityResponseDTO> response =
    // fetchLoanActivityResponses(Collections.singletonList(loanActivity));
    // return new BaseResponse<>(HttpStatus.OK, "查询成功", response.get(0));
    // }

    // @Timed("检查用户信息访问耗时")
    // @Counted("检查用户信息访问频率")
    public static CheckResult checkUserInfo(LoanRule loanRule, User user) {
        CheckResult baseResult = new CheckResult();
        baseResult.setResult(false);
        if (loanRule.getMaxAge() != null && user.getAge() >= loanRule.getMaxAge()) {
            baseResult.setMessage("用户年龄不能高于" + loanRule.getMaxAge());
            return baseResult;
        }
        if (loanRule.getMinAge() != null && user.getAge() < loanRule.getMinAge()) {
            baseResult.setMessage("用户年龄不能低于" + loanRule.getMinAge());
            return baseResult;
        }
        if (loanRule.getCheckCountry() != null && loanRule.getCheckCountry() && user.getCountry() != null
                && !user.getCountry().equals("中国")) {
            baseResult.setMessage("用户必须来自中国");
            return baseResult;
        }
        if (loanRule.getCheckDishonest() != null && loanRule.getCheckDishonest() && user.getDishonest()) {
            baseResult.setMessage("用户不能是失信人员");
            return baseResult;
        }
        if (loanRule.getCheckEmployment() != null && loanRule.getCheckEmployment()
                && user.getEmployment() != Employment.Employed) {
            baseResult.setMessage("用户必须在职");
            return baseResult;
        }
        if (loanRule.getCheckOverDual() != null && loanRule.getCheckOverDual() && user.getOverDual() != null
                && user.getOverDual() > 0) {
            baseResult.setMessage("用户的逾期记录不能超过 0 次");
            return baseResult;
        }
        baseResult.setResult(true);
        return baseResult;
    }

    public void saveCheckReslult(User user, Activity loanActivity, Boolean result) {
        List<UserActivity> userActivities = userActivityDao.findByUserIdAndActivityId(user.getId(),
                loanActivity.getId());
        System.out.println("findByUserAndLoanActivity: " + userActivities);
        if (userActivities.isEmpty()) {
            userActivityDao.saveAndFlush(
                    UserActivity.builder().userId(user.getId()).activityId(loanActivity.getId()).isPassed(result)
                            .build());
        }
        // else {
        // userLoanActivitys.get(0).setIsPassed(result);
        // System.out.println(userLoanActivitys.get(0).getId());
        // userLoanActivityDao.saveAndFlush(userLoanActivitys.get(0));
        // }
    }

    public boolean isRequestToFrequest(Long loanActivityId, Long userId) {
        // 用户限制请求频率
        String key = "REQUEST_LIMIT_COUNTER" + "." + userId + "." + loanActivityId;
        // String key = "tryjoin_" + loanActivityId + "_" +userId;
        Integer increase = (Integer) redisService.get(key);
        if (increase != null) {
            // 5 秒只能请求 1 次
            return true;

            // 1 分钟只能请求 5 次
            // if (increase < 5) {
            // redisService.incr(key, 1);
            // }else {
            // return true;
            // }
        } else {
            // redisService.set(key, 1, 60 * 1);
            redisService.set(key, 1, 5);
        }
        return false;
    }

    // @Timed
    public BaseResponse<Boolean> check(Long loanActivityId, Long userId) {
        Activity loanActivity = activityDao.findById(loanActivityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        if (!loanActivity.getType().equals(LOAN_ACTIVITY_TYPE)) {
            throw new DataRetrievalFailureException("没有该活动");
        }
        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
        LoanRule loanRule = loanRuleDao.findById(loanActivity.getRuleId())
                .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
        CheckResult checkResult = LoanActivityService.checkUserInfo(loanRule, user);
        // 数据库
        saveCheckReslult(user, loanActivity, checkResult.getResult());
        // redis
        stringRedisTemplate.opsForValue().set(USER_CHECK_LOAN_CACHE + "." + userId + "." + loanActivityId,
                checkResult.getResult() ? "1" : "0");
        if (!checkResult.getResult()) {
            return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + checkResult.getMessage(), false);
        }
        return new BaseResponse<>(HttpStatus.OK, "初筛通过", true);
    }

    // @Timed
    public BaseResponse<TryJoinResponseDTO> tryJoin(Long loanActivityId, Long userId, String account_sn) {
        TryJoinResponseDTO res = new TryJoinResponseDTO();
        res.setResult(4);
        try {
            // 用户限制请求频率
            if (isRequestToFrequest(loanActivityId, userId)) {
                res.setResult(3);
                return new BaseResponse<>(HttpStatus.OK, "请求频繁，请稍后再试", res);
            }

            // 判断用户是否参加过初筛
            String checkResultStr = stringRedisTemplate.opsForValue()
                    .get(USER_CHECK_LOAN_CACHE + "." + userId + "." + loanActivityId);
            System.out.println("checkResultStr: " + checkResultStr);
            if (checkResultStr != null && !checkResultStr.equals("1")) {
                return new BaseResponse<>(HttpStatus.OK, "初筛不通过", res);
            }

            // 获取商品 ID
            Activity loanActivity = activityDao.findById(loanActivityId)
                    .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
            if (!loanActivity.getType().equals(LOAN_ACTIVITY_TYPE)) {
                throw new DataRetrievalFailureException("没有该活动");
            }
            Long goodId = loanActivity.getGoodsId();
            res.setGoodId(goodId);

            // 如果没有初筛过，就先筛
            if (checkResultStr == null) {
                User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
                LoanRule loanRule = loanRuleDao.findById(loanActivity.getRuleId())
                        .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
                CheckResult checkResult = LoanActivityService.checkUserInfo(loanRule, user);
                saveCheckReslult(user, loanActivity, checkResult.getResult());
                if (!checkResult.getResult()) {
                    res.setResult(4);
                    return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + checkResult.getMessage(), res);
                }
            }

            // 获取随机字符串
            String random = stringRedisTemplate.opsForValue().get(ActivityTask.ACTIVITY_RANDOM_KEY + "." + goodId);
            if (random == null || random.isEmpty()) {
                return new BaseResponse<>(HttpStatus.OK, "活动没有开始", res);
            }
            System.out.println(random);
            res.setRandom(random);

            String last_req = stringRedisTemplate.opsForValue()
                    .get(USER_SEND_REQUEST_TIME_KEY + "." + +userId + "." + goodId);
            String md5 = stringRedisTemplate.opsForValue().get(USER_MD5_CACHE + "." + userId + "." + goodId);

            // 如果没拿到 md5 记录就重新生成
            if (last_req == null || md5 == null) {

                String time = String.valueOf(new Date().getTime());
                List<String> arrayList = Arrays.asList(AUTH_SALT, userId.toString(), goodId.toString(), account_sn,
                        time);
                md5 = MD5.md5(arrayList);
                res.setResult(0);
                res.setMd5(md5);
                // 缓存 MD5 生成时间
                stringRedisTemplate.opsForValue().set(USER_SEND_REQUEST_TIME_KEY + "." + +userId + "." + goodId, time);
                // 缓存 MD5
                stringRedisTemplate.opsForValue().set(USER_MD5_CACHE + "." + userId + "." + goodId, md5, 5,
                        TimeUnit.SECONDS);
                res.setResult(1);
                return new BaseResponse<>(HttpStatus.OK, "参加链接成功", res);
            }
            res.setResult(1);
            res.setMd5(md5);
            System.out.println("之前的 md5：" + md5);
            return new BaseResponse<>(HttpStatus.OK, "您已经参加过，返回之前的 md5", res);
        } catch (Exception e) {
            System.out.println("发生未知错误");
            e.printStackTrace();
            return new BaseResponse<>(HttpStatus.OK, "发生未知错误: " + e, res);
        }
    }

    public BaseResponse<Boolean> deleteActivity(Long id) {
        activityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", true);
    }

}