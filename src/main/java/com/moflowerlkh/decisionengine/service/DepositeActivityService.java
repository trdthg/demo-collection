package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.*;
import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;
import com.moflowerlkh.decisionengine.schedule.ActivityTask;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.CreateDepositActivityResponseDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.CreateDepositActivityRequestDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.GetActivityResponseDTO;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.*;
import com.moflowerlkh.decisionengine.util.MD5;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static com.moflowerlkh.decisionengine.service.ActivityService.DEPOSIT_ACTIVITY_TYPE;
import static com.moflowerlkh.decisionengine.service.LoanActivityService.*;

@Service
public class DepositeActivityService {
    @Autowired
    DepositRuleDao depositRuleDao;
    @Autowired
    ActivityDao activityDao;
    @Autowired
    GoodsDao goodsDao;
    @Autowired
    UserDao userDao;
    @Autowired
    BankAccountDao bankAccountDao;
    @Autowired
    UserActivityDao userActivityDao;
    @Autowired
    StringRedisTemplate stringRedisTemplate;
    @Autowired
    RedisService redisService;
    public static final String USER_CHECK_DEPOSIT_CACHE = "USER_CHECK_DEPOSIT_CACHE";

    public BaseResponse<GetActivityResponseDTO> create(CreateDepositActivityRequestDTO request) {
        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
            .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        User user = userDao.getById(loginUser.getId());
        List<BankAccount> accounts = bankAccountDao.findByUserID(user.getId());
        if (accounts.isEmpty()) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "您需要有至少一张银行卡", null);
        }

        // 规则
        DepositRule rule = new DepositRule();
        rule.setTimeLimit(request.getActivity_timeLimit());
        rule.setApr(request.getActivity_apr());
        //#3
        rule.setPurchasersNumberLimit(request.getActivity_totalQuantity());
        rule.setMaxAge(request.getRule().getActivity_ageUp());
        rule.setMinAge(request.getRule().getActivity_ageFloor());
        rule.setIdDawa(request.getRule().getActivity_dawa());
        rule.setIsOnDay(request.getRule().getActivity_dateRate());
        depositRuleDao.save(rule);

        // 商品
        Goods goods = new Goods();
        goods.setPrice(request.getActivity_perPrice());
        //#1
        goods.setGoodsAmount(request.getActivity_totalQuantity() * request.getActivity_oneMaxAmount());
        //#2
        goods.setOneMaxAmount(request.getActivity_oneMaxAmount());
        goods.setStartTime(Timestamp.valueOf(request.getActivity_startTime()));
        goods.setBankAccountSN(accounts.get(0).getBankAccountSN());
        goodsDao.save(goods);

        // 活动
        Activity activity = new Activity();
        activity.setName(request.getActivity_name());
        activity.setBeginTime(Timestamp.valueOf(request.getActivity_startTime()));
        activity.setEndTime(Timestamp.valueOf(request.getActivity_endTime()));

        activity.setRuleId(rule.getId());
        activity.setGoodsId(goods.getId());

        activity.setType(2);
        activityDao.save(activity);

        stringRedisTemplate.opsForValue().set(ScheduleKey + "." + activity.getId(),
            String.valueOf(new Date().getTime()));
        System.out.println(stringRedisTemplate.opsForValue().get(ScheduleKey + "." + activity.getId()));

        CreateDepositActivityResponseDTO response = new CreateDepositActivityResponseDTO();
        response.setId(activity.getId().toString());
        response.setGood_id(activity.getGoodsId().toString());

        GetActivityResponseDTO res = GetActivityResponseDTO.from(activity, rule, goods);
        return new BaseResponse<>(HttpStatus.OK, "创建成功", res);
    }

    public BaseResponse<GetActivityResponseDTO> update(Long id, CreateDepositActivityRequestDTO request) {
        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
            .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        User user = userDao.getById(loginUser.getId());
        List<BankAccount> accounts = bankAccountDao.findByUserID(user.getId());
        if (accounts.isEmpty()) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "您需要有至少一张银行卡", null);
        }

        // 活动
        Activity activity = activityDao.findById(id).orElseThrow(()-> new DataRetrievalFailureException("没有该活动"));
        activity.setName(request.getActivity_name());
        activity.setBeginTime(Timestamp.valueOf(request.getActivity_startTime()));
        activity.setEndTime(Timestamp.valueOf(request.getActivity_endTime()));

        activityDao.saveAndFlush(activity);

        // 规则
        DepositRule rule = depositRuleDao.findById(activity.getRuleId()).orElseThrow(()->new RuntimeException("没有对应的规则"));
        rule.setPurchasersNumberLimit(request.getActivity_totalQuantity());
        rule.setApr(request.getActivity_apr());
        rule.setTimeLimit(request.getActivity_timeLimit());
        rule.setMaxAge(request.getRule().getActivity_ageUp());
        rule.setMinAge(request.getRule().getActivity_ageFloor());
        rule.setIdDawa(request.getRule().getActivity_dawa());
        rule.setIsOnDay(request.getRule().getActivity_dateRate());
        depositRuleDao.saveAndFlush(rule);

        // 商品
        Goods goods = goodsDao.findById(activity.getGoodsId()).orElseThrow(()->new RuntimeException("没有对应商品"));
        goods.setPrice(request.getActivity_perPrice());
        goods.setGoodsAmount(request.getActivity_totalQuantity());
        goods.setStartTime(Timestamp.valueOf(request.getActivity_startTime()));
        goods.setOneMaxAmount(request.getActivity_oneMaxAmount());
        goods.setBankAccountSN(accounts.get(0).getBankAccountSN());
        goodsDao.saveAndFlush(goods);

        CreateDepositActivityResponseDTO response = new CreateDepositActivityResponseDTO();
        response.setId(activity.getId().toString());
        response.setGood_id(activity.getGoodsId().toString());

        GetActivityResponseDTO res = GetActivityResponseDTO.from(activity, rule, goods);

        return new BaseResponse<>(HttpStatus.OK, "创建成功", res);
    }

    public BaseResponse<PageResult<List<GetActivityResponseDTO>>> findByPage(Integer page_num, Integer page_limit) {
        Page<Activity> activities = activityDao
            .findAllByType(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")), DEPOSIT_ACTIVITY_TYPE);
        Integer pages = activities.getTotalPages();
        List<GetActivityResponseDTO> res = activities.toList().stream().filter(x -> x.getType().equals(2)).map(x -> {
            DepositRule rule = depositRuleDao.getById(x.getRuleId());
            Goods goods = goodsDao.getById(x.getGoodsId());
            return GetActivityResponseDTO.from(x, rule, goods);
        }).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<GetActivityResponseDTO> findById(Long id) {
        Activity activity = activityDao.findById(id).orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        if (!activity.getType().equals(DEPOSIT_ACTIVITY_TYPE)) {
            throw new DataRetrievalFailureException("没有该活动");
        }
        DepositRule rule = depositRuleDao.getById(activity.getRuleId());
        Goods goods = goodsDao.getById(activity.getGoodsId());
        GetActivityResponseDTO res = GetActivityResponseDTO.from(activity, rule, goods);
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }


    public BaseResponse<Boolean> deleteById(Long id) {
        activityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", true);
    }

    public BaseResponse<Boolean> check(Long user_id, Long activity_id) {
        User user = userDao.findById(user_id).orElseThrow(()-> new DataRetrievalFailureException("没有该用户"));
        Activity activity = activityDao.findById(activity_id).orElseThrow(()-> new DataRetrievalFailureException("没有该活动"));
        if (!activity.getType().equals(DEPOSIT_ACTIVITY_TYPE)) {
            throw new DataRetrievalFailureException("没有该活动");
        }
        CheckResult checkResult = checkUserInfo(user, activity);
        saveCheckReslult(user,activity,checkResult.getResult());
        stringRedisTemplate.opsForValue().set(USER_CHECK_DEPOSIT_CACHE + "." + user.getId() + "." + activity.getId(), checkResult.getResult() ? "1" : "0");
        if (!checkResult.getResult()) {
            return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + checkResult.getMessage(), false);
        }
        return new BaseResponse<>(HttpStatus.OK, "初筛通过", true);
    }

    public void saveCheckReslult(User user, Activity activity, Boolean result) {
        List<UserActivity> userActivities = userActivityDao.findByUserIdAndActivityId(user.getId(), activity.getId());
        if (userActivities.isEmpty()) {
            activityDao.saveAndFlush(activity);
            userActivityDao.saveAndFlush(
                UserActivity.builder().userId(user.getId()).activityId(activity.getId()).isPassed(result)
                    .build());
        }
    }

    public CheckResult checkUserInfo(User user, Activity activity) {
        if (!activity.getType().equals(DEPOSIT_ACTIVITY_TYPE)) {
            throw new DataRetrievalFailureException("没有该活动");
        }
        DepositRule rule = depositRuleDao.findById(activity.getRuleId()).orElseThrow(()->new DataRetrievalFailureException("查询活动规则失败"));
        CheckResult result = new CheckResult();
        result.setResult(false);
        if (rule.getMaxAge() != null && user.getAge() >= rule.getMaxAge()) {
            result.setMessage("年龄超过了" + rule.getMaxAge());
            return result;
        }
        if (rule.getMinAge() != null && user.getAge() < user.getAge()) {
            result.setMessage("年龄不能低于" + rule.getMaxAge());
            return result;
        }
        if (rule.getCheckDishonest() != null && rule.getCheckDishonest() && !user.getDishonest()) {
            result.setMessage("失信人员禁止参加");
            return result;
        }

        if (rule.getCheckEmployment() != null && rule.getCheckEmployment() && user.getEmployment() != Employment.Employed) {
            result.setMessage("用户必须在职");
            return result;
        }
        result.setResult(true);
        return result;
    }

    public boolean isRequestToFrequest(Long loanActivityId, Long userId) {
        // 用户限制请求频率
        String key = "REQUEST_LIMIT_COUNTER" + "." + userId;
        Integer increase = (Integer) redisService.get(key);
        if (increase != null) {
            return true;
        } else {
            redisService.set(key, 1, 3);
        }
        return false;
    }
    public BaseResponse<TryJoinResponseDTO> tryJoin(Long depositActivityId, Long userId, String account_sn) {
        TryJoinResponseDTO res = new TryJoinResponseDTO();
        res.setResult(4);
        try {
            // 用户限制请求频率
            if (isRequestToFrequest(depositActivityId, userId)) {
                res.setResult(3);
                return new BaseResponse<>(HttpStatus.OK, "请求频繁，请稍后再试", res);
            }

            // 判断用户是否参加过初筛
            String checkResultStr = stringRedisTemplate.opsForValue().get(USER_CHECK_DEPOSIT_CACHE + "." + userId + "." + depositActivityId);
            System.out.println("checkResultStr: " + checkResultStr);
            if (checkResultStr != null && !checkResultStr.equals("1")) {
                return new BaseResponse<>(HttpStatus.OK, "初筛不通过", res);
            }

            // 获取商品 ID
            Activity activity = activityDao.findById(depositActivityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
            if (!activity.getType().equals(DEPOSIT_ACTIVITY_TYPE)) {
                throw new DataRetrievalFailureException("没有该活动");
            }
            Long goodId = activity.getGoodsId();
            res.setGoodId(goodId);

            // 如果没有初筛过，就先筛
            if (checkResultStr == null) {
                User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
                DepositRule depositRule = depositRuleDao.findById(activity.getRuleId())
                    .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
                CheckResult checkResult = checkUserInfo(user, activity);
                saveCheckReslult(user, activity, checkResult.getResult());
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

            String last_req = stringRedisTemplate.opsForValue().get(USER_SEND_REQUEST_TIME_KEY + "." + +userId + "." + goodId);
            String md5 = stringRedisTemplate.opsForValue().get(USER_MD5_CACHE + "." + userId + "." + goodId);

            // 如果没拿到 md5 记录就重新生成
            if (last_req == null || md5 == null) {

                String time = String.valueOf(new Date().getTime());
                List<String> arrayList = Arrays.asList(AUTH_SALT, userId.toString(), goodId.toString(),account_sn, time);
                md5 = MD5.md5(arrayList);
                res.setResult(0);
                res.setMd5(md5);
                // 缓存 MD5 生成时间
                stringRedisTemplate.opsForValue().set(USER_SEND_REQUEST_TIME_KEY + "." + +userId + "." + goodId, time);
                // 缓存 MD5
                stringRedisTemplate.opsForValue().set(USER_MD5_CACHE + "." + userId + "." + goodId, md5, 5, TimeUnit.SECONDS);
                res.setResult(1);
                return new BaseResponse<>(HttpStatus.OK, "参加链接成功", res);
            }
            res.setResult(1);
            res.setMd5(md5);
            System.out.println("之前的 md5：" + md5);
            return new BaseResponse<>(HttpStatus.OK, "您已经参加过, 返回之前的 md5", res);
        } catch (Exception e){
            System.out.println("发生未知错误");
            e.printStackTrace();
            return new BaseResponse<>(HttpStatus.OK, "发生未知错误: " + e, res);
        }
    }

}
