package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.*;
import com.moflowerlkh.decisionengine.domain.entities.activities.DepositActivity;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.DepositRule;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.schedule.ActivityTask;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.CreateDepositActivityResponseDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.CreateDepositActivityRequestDTO;
import com.moflowerlkh.decisionengine.service.DepositeActivityDTO.DepositActivitySimpleResponseDTO;
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

import static com.moflowerlkh.decisionengine.service.LoanActivityService.*;

@Service
public class DepositeActivityService {
    @Autowired
    DepositRuleDao depositRuleDao;
    @Autowired
    DepositActivityDao depositActivityDao;
    @Autowired
    GoodsDao goodsDao;
    @Autowired
    UserDao userDao;
    @Autowired
    BankAccountDao bankAccountDao;
    @Autowired
    UserDepositActivityDao userDepositActivityDao;
    @Autowired
    StringRedisTemplate stringRedisTemplate;
    @Autowired
    RedisService redisService;
    public static final String USER_CHECK_DEPOSIT_CACHE = "USER_CHECK_DEPOSIT_CACHE";

    public BaseResponse<CreateDepositActivityResponseDTO> create(CreateDepositActivityRequestDTO request) {
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
        rule.setMaxAge(request.getRule().getActivity_ageUp());
        rule.setMinAge(request.getRule().getActivity_ageFloor());
        rule.setIdDawa(request.getRule().getActivity_dawa());
        rule.setIsOnDay(request.getRule().getActivity_dateRate());
        depositRuleDao.save(rule);

        // 商品
        Goods goods = new Goods();
        goods.setPrice(request.getPerPrice());
        goods.setGoodsAmount(request.getActivity_totalQuantity());
        goods.setStartTime((Timestamp) request.getActivity_startTime());
        goods.setOneMaxAmount(request.getActivity_oneMaxAmount());
        goods.setBankAccountSN(accounts.get(0).getBankAccountSN());
        goodsDao.save(goods);

        // 活动
        DepositActivity depositActivity = new DepositActivity();
        depositActivity.setName(request.getActivity_name());
        depositActivity.setApr(request.getActivity_apr());
        depositActivity.setTimeLimit(request.getActivity_timeLimit());
        depositActivity.setBeginTime((Timestamp) request.getActivity_startTime());
        depositActivity.setEndTime((Timestamp) request.getActivity_endTime());

        depositActivity.setDepositRuleId(rule.getId());
        depositActivity.setGoodsId(goods.getId());
        depositActivityDao.save(depositActivity);

        stringRedisTemplate.opsForValue().set(ScheduleKey + "." + depositActivity.getId(),
            String.valueOf(new Date().getTime()));

        CreateDepositActivityResponseDTO response = new CreateDepositActivityResponseDTO();
        response.setId(depositActivity.getId().toString());
        response.setGood_id(depositActivity.getGoodsId().toString());
        return new BaseResponse<>(HttpStatus.OK, "创建成功", response);
    }

    public BaseResponse<CreateDepositActivityResponseDTO> update(Long id, CreateDepositActivityRequestDTO request) {
        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
            .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        User user = userDao.getById(loginUser.getId());
        List<BankAccount> accounts = bankAccountDao.findByUserID(user.getId());
        if (accounts.isEmpty()) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "您需要有至少一张银行卡", null);
        }

        // 活动
        DepositActivity depositActivity = depositActivityDao.findById(id).orElseThrow(()-> new DataRetrievalFailureException("没有该活动"));
        depositActivity.setName(request.getActivity_name());
        depositActivity.setApr(request.getActivity_apr());
        depositActivity.setTimeLimit(request.getActivity_timeLimit());
        depositActivity.setBeginTime((Timestamp) request.getActivity_startTime());
        depositActivity.setEndTime((Timestamp) request.getActivity_endTime());

        depositActivityDao.saveAndFlush(depositActivity);

        // 规则
        DepositRule rule = depositRuleDao.findById(depositActivity.getDepositRuleId()).orElseThrow(()->new RuntimeException("没有对应的规则"));
        rule.setMaxAge(request.getRule().getActivity_ageUp());
        rule.setMinAge(request.getRule().getActivity_ageFloor());
        rule.setIdDawa(request.getRule().getActivity_dawa());
        rule.setIsOnDay(request.getRule().getActivity_dateRate());
        depositRuleDao.saveAndFlush(rule);

        // 商品
        Goods goods = goodsDao.findById(depositActivity.getDepositRuleId()).orElseThrow(()->new RuntimeException("没有对应商品"));
        goods.setPrice(request.getPerPrice());
        goods.setGoodsAmount(request.getActivity_totalQuantity());
        goods.setStartTime((Timestamp) request.getActivity_startTime());
        goods.setOneMaxAmount(request.getActivity_oneMaxAmount());
        goods.setBankAccountSN(accounts.get(0).getBankAccountSN());
        goodsDao.saveAndFlush(goods);

        CreateDepositActivityResponseDTO response = new CreateDepositActivityResponseDTO();
        response.setId(depositActivity.getId().toString());
        response.setGood_id(depositActivity.getGoodsId().toString());
        return new BaseResponse<>(HttpStatus.OK, "创建成功", response);
    }

    public BaseResponse<PageResult<List<DepositActivity>>> findByPage(Integer page_num, Integer page_limit) {
        Page<DepositActivity> depositActivities = depositActivityDao
            .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")));
        Integer pages = depositActivities.getTotalPages();
        List<DepositActivity> res = depositActivities.toList();
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<DepositActivity> findById(Long id) {
        DepositActivity depositActivity = depositActivityDao.findById(id).orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", depositActivity);
    }


    public BaseResponse<Boolean> deleteById(Long id) {
        depositActivityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", true);
    }

    public BaseResponse<Boolean> check(Long user_id, Long activity_id) {
        User user = userDao.findById(user_id).orElseThrow(()-> new DataRetrievalFailureException("没有该用户"));
        DepositActivity activity = depositActivityDao.findById(activity_id).orElseThrow(()-> new DataRetrievalFailureException("没有该活动"));
        CheckResult checkResult = checkUserInfo(user, activity);
        saveCheckReslult(user,activity,checkResult.getResult());
        stringRedisTemplate.opsForValue().set(USER_CHECK_DEPOSIT_CACHE + "." + user.getId() + "." + activity.getId(), checkResult.getResult() ? "1" : "0");
        if (!checkResult.getResult()) {
            return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + checkResult.getMessage(), false);
        }
        return new BaseResponse<>(HttpStatus.OK, "初筛通过", true);
    }

    public void saveCheckReslult(User user, DepositActivity depositActivity, Boolean result) {
        Set<Long> userIds = depositActivity.getUserIds();
        if (!userIds.contains(user.getId())) {
            userIds.add(user.getId());
            depositActivityDao.saveAndFlush(depositActivity);
            userDepositActivityDao.saveAndFlush(
                UserDepositActivity.builder().userId(user.getId()).activityId(depositActivity.getId()).isPassed(result)
                    .build());
        }
    }

    public CheckResult checkUserInfo(User user, DepositActivity activity) {
        DepositRule rule = depositRuleDao.findById(activity.getDepositRuleId()).orElseThrow(()->new DataRetrievalFailureException("查询活动规则失败"));
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
        if (rule.getCheckDishonest() != null && !user.getDishonest()) {
            result.setMessage("失信人员禁止参加");
            return result;
        }

        if (rule.getCheckEmployment() != null && user.getEmployment() != Employment.Employed) {
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
    public BaseResponse<TryJoinResponse> tryJoin(Long depositActivityId, Long userId, String account_sn) {
        TryJoinResponse res = new TryJoinResponse();
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
            DepositActivity depositActivity = depositActivityDao.findById(depositActivityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
            Long goodId = depositActivity.getGoodsId();
            res.setGoodId(goodId);

            // 如果没有初筛过，就先筛
            if (checkResultStr == null) {
                User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
                DepositRule depositRule = depositRuleDao.findById(depositActivity.getDepositRuleId())
                    .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
                CheckResult checkResult = checkUserInfo(user, depositActivity);
                saveCheckReslult(user, depositActivity, checkResult.getResult());
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
                ArrayList<String> arrayList = (ArrayList<String>) Arrays.asList(AUTH_SALT, userId.toString(), goodId.toString(),account_sn, time);
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
