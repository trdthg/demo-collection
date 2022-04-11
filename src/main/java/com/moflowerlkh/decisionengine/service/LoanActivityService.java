package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.*;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.schedule.ActivityTask;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.*;
import com.moflowerlkh.decisionengine.util.CodeResult;
import com.moflowerlkh.decisionengine.util.JwtUtil;
import com.moflowerlkh.decisionengine.util.MD5;
import com.moflowerlkh.decisionengine.util.ValidateCode;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.PageResult;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.po.BaseResult;
import io.micrometer.core.annotation.Counted;
import io.micrometer.core.annotation.Timed;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import javax.validation.Valid;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class LoanActivityService {
    @Autowired
    LoanActivityDao loanActivityDao;
    @Autowired
    GoodsDao goodsDao;
    @Autowired
    LoanRuleDao loanRuleDao;
    @Autowired
    UserDao userDao;
    @Autowired
    UserLoanActivityDao userLoanActivityDao;
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
    public static final String USER_CHECK_CACHE = "USER_CHECK_CACHE";
    public static final String USER_MD5_CACHE = "USER_MD5_CACHE";
    public BaseResponse<LoanActivityResponse> setLoanActivity(@RequestBody @Valid SetLoanActivityRequest request) {

        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
            .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        User user = loginUser.getUser();
        List<BankAccount> accounts = bankAccountDao.findByUserID(user.getId());
        if (accounts.isEmpty()) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "您需要有至少一张银行卡", null);
        }
        LoanActivity loanActivity = request.toLoanActivity();

        Goods goods = new Goods();
        goods.setStartTime(loanActivity.getBeginTime());
        goods.setBankAccountSN(accounts.get(0).getBankAccountSN());
        goods.setPrice(request.getActivity_perPrice());
        goods.setOneMaxAmount(1);
        goods.setGoodsAmount(request.getActivity_totalQuantity());
        goodsDao.save(goods);

        LoanRule loanRule = request.getRule().toLoanRule();
        loanRuleDao.save(loanRule);

        loanActivity.setGoodsId(goods.getId());
        loanActivity.setLoanRuleId(loanRule.getId());
        // 新建活动
        loanActivityDao.save(loanActivity);

        // 保存开始时间
        stringRedisTemplate.opsForValue().set(ScheduleKey + "." + loanActivity.getId(),
                String.valueOf(new Date().getTime()));

        LoanActivityResponse res = LoanActivityResponse.fromLoanActivity(loanActivity);
        res.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanRule));
        return new BaseResponse<>(HttpStatus.CREATED, "新增成功", res);
    }

    public BaseResponse<LoanActivityResponse> changeActivityInfo(Long id, SetLoanActivityRequest request) {
        LoanActivity newLoanActivity = request.toLoanActivity();
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动失败"));
        LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId())
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动规则失败"));
        Goods goods = goodsDao.findById(loanActivity.getGoodsId())
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动对应的商品失败"));
        newLoanActivity.setLoanRuleId(loanRule.getId());
        newLoanActivity.setGoodsId(goods.getId());
        loanActivityDao.saveAndFlush(newLoanActivity);

        goods.setStartTime(loanActivity.getBeginTime());
        goods.setOneMaxAmount(1);
        goods.setGoodsAmount(request.getActivity_totalQuantity());
        goodsDao.saveAndFlush(goods);

        LoanRule loanRule1 = request.getRule().toLoanRule();
        loanRule1.setId(loanRule.getId());
        loanRuleDao.saveAndFlush(loanRule1);
        return new BaseResponse<>(HttpStatus.OK, "修改成功", LoanActivityResponse.fromLoanActivity(loanActivity));
    }

    public BaseResponse<PageResult<List<LoanActivitySimpleResponse>>> findAllActivityPartial(Integer page_num,
            Integer page_limit) {
        Page<LoanActivity> loanActivities = loanActivityDao
                .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")));
        Integer pages = loanActivities.getTotalPages();
        List<LoanActivitySimpleResponse> res = loanActivities.stream().map(loanActivity -> {
                LoanActivitySimpleResponse response = LoanActivitySimpleResponse.fromLoanActivity(loanActivity);
                Goods goods = goodsDao.findById(loanActivity.getGoodsId()).orElseThrow(() -> new DataRetrievalFailureException("活动没有对应的商品"));
                response.setPerPrice(goods.getPrice());
                response.setOneMaxAmount(goods.getOneMaxAmount());
                return response;
            })
                .collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<LoanActivitySimpleResponse> findByIdPartial(Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
            .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId()).orElseThrow(() -> new DataRetrievalFailureException("查询该活动规则失败"));
        LoanActivitySimpleResponse response = LoanActivitySimpleResponse.fromLoanActivity(loanActivity);
        response.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanRule));

        Goods goods = goodsDao.findById(loanActivity.getGoodsId()).orElseThrow(() -> new DataRetrievalFailureException("活动没有对应的商品"));
        response.setPerPrice(goods.getPrice());
        response.setOneMaxAmount(goods.getOneMaxAmount());

        return new BaseResponse<>(HttpStatus.OK, "查询成功", response);
    }

    public BaseResponse<PageResult<List<LoanActivityResponse>>> findAllActivity(Integer page_num, Integer page_limit) {
        Page<LoanActivity> loanActivities = loanActivityDao
                .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")));
        Integer pages = loanActivities.getTotalPages();
        List<LoanActivityResponse> res = loanActivities.stream().map(loanActivity -> {
                LoanActivityResponse response = LoanActivityResponse.fromLoanActivity(loanActivity);
                Set<UserLoanActivity> userLoanActivities = loanActivity.getUserLoanActivities();
                response.setPassed_users(userLoanActivities.stream().filter(UserLoanActivity::getIsPassed).map(x -> JoinLoanActivityUserResponse.fromUser(x.getUser())).collect(Collectors.toList()));
                response.setUnPassed_users(userLoanActivities.stream().filter(x -> !x.getIsPassed()).map(x -> JoinLoanActivityUserResponse.fromUser(x.getUser())).collect(Collectors.toList()));

                Goods goods = goodsDao.findById(loanActivity.getGoodsId()).orElseThrow(() -> new DataRetrievalFailureException("活动没有对应的商品"));
                response.setPerPrice(goods.getPrice());
                response.setOneMaxAmount(goods.getOneMaxAmount());
                return response;
            }).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<LoanActivityResponse> findById(Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
            .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));

        LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId()).orElseThrow(() -> new DataRetrievalFailureException("查询该活动规则失败"));
        LoanActivityResponse response = LoanActivityResponse.fromLoanActivity(loanActivity);
        response.setRule(SetLoanActivityRuleRequest.fromLoanRule(loanRule));

        Set<UserLoanActivity> userLoanActivities = loanActivity.getUserLoanActivities();
        response.setPassed_users(userLoanActivities.stream().filter(UserLoanActivity::getIsPassed).map(x -> JoinLoanActivityUserResponse.fromUser(x.getUser())).collect(Collectors.toList()));
        response.setUnPassed_users(userLoanActivities.stream().filter(x -> !x.getIsPassed()).map(x -> JoinLoanActivityUserResponse.fromUser(x.getUser())).collect(Collectors.toList()));

        Goods goods = goodsDao.findById(loanActivity.getGoodsId()).orElseThrow(() -> new DataRetrievalFailureException("活动没有对应的商品"));
        response.setPerPrice(goods.getPrice());
        response.setOneMaxAmount(goods.getOneMaxAmount());

        return new BaseResponse<>(HttpStatus.OK, "查询成功", response);
    }

    @Timed("检查用户信息访问耗时")
    @Counted("检查用户信息访问频率")
    public BaseResult<Boolean> checkUserInfo(LoanActivity loanActivity, LoanRule loanRule, User user) {
        BaseResult<Boolean> baseResult = new BaseResult<>();
        baseResult.setResult(false);
        if (loanRule.getMaxAge() != null && user.getAge() >= loanRule.getMaxAge()) {
            baseResult.setMessage("用户年龄不能高于" + loanRule.getMaxAge());
            return baseResult;
        }
        if (loanRule.getMinAge() != null && user.getAge() < loanRule.getMinAge()) {
            baseResult.setMessage("用户年龄不能低于" + loanRule.getMinAge());
            return baseResult;
        }
        if (loanRule.getCheckCountry() && (!Objects.equals(user.getCountry(), "中国"))) {
            baseResult.setMessage("用户必须来自中国");
            return baseResult;
        }
        if (loanRule.getCheckDishonest() && user.getDishonest()) {
            baseResult.setMessage("用户不能是失信人员");
            return baseResult;
        }
        if (loanRule.getCheckEmployment() && user.getEmployment() != Employment.Employed) {
            baseResult.setMessage("用户必须在值");
            return baseResult;
        }
        if (loanRule.getCheckOverDual() && user.getOverDual() != null && user.getOverDual() > 0) {
            baseResult.setMessage("用户的逾期记录不能超过 0 次");
            return baseResult;
        }
        baseResult.setResult(true);
        return baseResult;
    }

    public boolean isRequestToFrequest(Long loanActivityId, Long userId) {
        // 用户限制请求频率
        String key = "" + userId + "_" + loanActivityId + "_request_count";
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

    public BaseResponse<Boolean> check(Long loanActivityId, Long userId) {
        LoanActivity loanActivity = loanActivityDao.findById(loanActivityId)
            .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        Long goodId = loanActivity.getGoodsId();

        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
        LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId())
            .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
        BaseResult<Boolean> baseResult = new LoanActivityService().checkUserInfo(loanActivity, loanRule, user);
        userLoanActivityDao.saveAndFlush(
            UserLoanActivity.builder().user(user).loanActivity(loanActivity).isPassed(baseResult.getResult())
                .build());
        stringRedisTemplate.opsForValue().set(USER_CHECK_CACHE + "." + userId + "." + loanActivityId, "1");
        if (!baseResult.getResult()) {
            return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + baseResult.getMessage(), false);
        }
        return new BaseResponse<>(HttpStatus.OK, "初筛通过", true);
    }

    @Timed("写入数据库耗时")
    @Counted("写入数据库频率")
    public BaseResponse<TryJoinResponse> tryJoin(Long loanActivityId, Long userId, Long account_id) {
        TryJoinResponse res = new TryJoinResponse();
        res.setResult(4);
        // 用户限制请求频率
        if (isRequestToFrequest(loanActivityId, userId)) {
            res.setResult(3);
            return new BaseResponse<>(HttpStatus.OK, "请求频繁，请稍后再试", res);
        }

        // 校验验证吗
        //String cachedCodeKey = "" + userId + "_tryjoin_code";
        //String cachedCode = (String) redisService.get(cachedCodeKey);
        //if (cachedCode != null && varifyCode != null && !cachedCode.equals(varifyCode)) {
        //    return new BaseResponse<>(HttpStatus.BAD_REQUEST, "验证码错误", res);
        //}

        // 判断用户是否参加过活动
        String checkResultStr = stringRedisTemplate.opsForValue().get(USER_CHECK_CACHE + "." + userId + "." + loanActivityId);
        System.out.println("checkResultStr: " + checkResultStr);
        // 如果没有初筛过，就先筛
        if (checkResultStr == null || checkResultStr.isEmpty()) {

            LoanActivity loanActivity = loanActivityDao.findById(loanActivityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
            Long goodId = loanActivity.getGoodsId();

            User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
            LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId())
                .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
            BaseResult<Boolean> baseResult = new LoanActivityService().checkUserInfo(loanActivity, loanRule, user);
            List<UserLoanActivity> userLoanActivitys = userLoanActivityDao.findByUserAndLoanActivity(user, loanActivity);
            System.out.println(userLoanActivitys);
            if (userLoanActivitys.isEmpty()) {
                userLoanActivityDao.saveAndFlush(
                    UserLoanActivity.builder().user(user).loanActivity(loanActivity).isPassed(baseResult.getResult())
                        .build());
            } else {
                userLoanActivitys.get(0).setIsPassed(baseResult.getResult());
                System.out.println(userLoanActivitys.get(0).getId());
                userLoanActivityDao.saveAndFlush(userLoanActivitys.get(0));
            }
            stringRedisTemplate.opsForValue().set(USER_CHECK_CACHE + "." + userId + "." + loanActivityId, "1");
            if (!baseResult.getResult()) {
                res.setResult(4);
                return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + baseResult.getMessage(), res);
            } else {
                stringRedisTemplate.opsForValue().set(USER_CHECK_CACHE + "." + userId + "." + loanActivityId, "0");
            }
        }
        // 获取商品 ID
        LoanActivity loanActivity = loanActivityDao.findById(loanActivityId)
            .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        Long goodId = loanActivity.getGoodsId();
        res.setGoodId(goodId);

        // 获取随机字符串
        String random = stringRedisTemplate.opsForValue().get(ActivityTask.ACTIVITY_RANDOM_KEY + "." + goodId);
        if (random == null || random.isEmpty()) {
            return new BaseResponse<>(HttpStatus.OK, "活动没有开始", res);
        }
        System.out.println(random);
        res.setRandom(random);

        String md5 = stringRedisTemplate.opsForValue().get(USER_MD5_CACHE + "." + userId + "." + loanActivityId);
        // 如果没拿到 md5 记录就重新生成
        if (md5 == null) {
            ArrayList<String> arrayList = new ArrayList<>();
            String time = String.valueOf(new Date().getTime());
            arrayList.add(AUTH_SALT);
            arrayList.add(userId.toString());
            arrayList.add(goodId.toString());
            arrayList.add(account_id.toString());
            arrayList.add(time);
            md5 = MD5.md5(arrayList);
            res.setResult(0);
            res.setMd5(md5);
            // 缓存 MD5 生成时间
            stringRedisTemplate.opsForValue().set(USER_SEND_REQUEST_TIME_KEY + "." + + userId + "." + goodId, time);
            // 缓存 MD5
            stringRedisTemplate.opsForValue().set(USER_MD5_CACHE + "." + userId + "." + loanActivityId, md5, 5);
            res.setResult(1);
            return new BaseResponse<>(HttpStatus.OK, "参加链接成功", res);
        }
        res.setResult(2);
        res.setMd5(md5);
        System.out.println("之前的 md5：" + md5);
        return new BaseResponse<>(HttpStatus.OK, "您已经参加过", res);
    }

    public BaseResponse<List<JoinLoanActivityUserResponse>> getPassedUsers(Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        List<JoinLoanActivityUserResponse> res = loanActivity.getUserLoanActivities().stream()
                .filter(x -> x.getIsPassed()).map(x -> x.getUser())
                .map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }

    public BaseResponse<List<JoinLoanActivityUserResponse>> getUnPassedUsers(Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        List<JoinLoanActivityUserResponse> res = loanActivity.getUserLoanActivities().stream()
                .filter(x -> !x.getIsPassed()).map(x -> x.getUser())
                .map(JoinLoanActivityUserResponse::fromUser).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }

    public BaseResponse<JoinLoanActivityUserResponse> getPassedUser(Long activity_id, String name) {
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

    public BaseResponse<JoinLoanActivityUserResponse> getUser(Long activity_id, Long user_id) {
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

    public BaseResponse<Boolean> deleteActivity(Long id) {
        loanActivityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", true);
    }

    public BaseResponse<String> generateCaptchaBase64() {
        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
                .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        Long userid = loginUser.getUser().getId();
        CodeResult codeResult = ValidateCode.getRandomCodeBase64();
        String key = "" + userid + "_tryjoin_code";
        redisService.set(key, codeResult.getRendom_string(), 60);
        String url = "data:image/png;base64," + codeResult.getBase64String();
        return new BaseResponse<>(HttpStatus.OK, "验证吗图片获取成功", url);
    }

}