package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.schedule.ActivityTask;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.LoanActivityResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.LoanActivitySimpleResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.SetLoanActivityRequest;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.SetLoanActivityRuleRequest;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.TryJoinResponse;
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

    public static final String ScheduleKey = "SCHEDULE_KEY";
    public static final String ACTIVITY_TO_GOODS_KEY = "ACTIVITY_TO_GOODS_KEY";
    public static final String AUTH_SALT = "bc30a3c8-b96b-49d2-bb9f-1c28f9408eb3";
    public static final String USER_SEND_REQUEST_TIME_KEY = "USER_SEND_REQUEST_TIME_KEY";
    public BaseResponse<LoanActivityResponse> setLoanActivity(@RequestBody @Valid SetLoanActivityRequest request) {

        LoanActivity loanActivity = request.toLoanActivity();

        Goods goods = new Goods();
        goods.setStartTime(loanActivity.getBeginTime());
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
        List<LoanActivitySimpleResponse> res = loanActivities.stream().map(LoanActivitySimpleResponse::fromLoanActivity)
                .collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<PageResult<List<LoanActivityResponse>>> findAllActivity(Integer page_num, Integer page_limit) {
        Page<LoanActivity> loanActivities = loanActivityDao
                .findAll(PageRequest.of(page_num - 1, page_limit, Sort.by(Sort.Direction.ASC, "id")));
        Integer pages = loanActivities.getTotalPages();
        List<LoanActivityResponse> res = loanActivities.stream().map(LoanActivityResponse::fromLoanActivity)
                .collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", new PageResult<>(res, pages));
    }

    public BaseResponse<LoanActivitySimpleResponse> findByIdPartial(Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", LoanActivitySimpleResponse.fromLoanActivity(loanActivity));
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
            baseResult.setMessage("用户的逾期记录不能超过0次");
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
            // 5秒只能请求1次
            return true;

            // 1分钟只能请求5次
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

    @Timed("写入数据库耗时")
    @Counted("写入数据库频率")
    public BaseResponse<TryJoinResponse> tryJoin(Long loanActivityId, Long userId) {
        TryJoinResponse res = new TryJoinResponse();
        res.setResult(false);
        // 用户限制请求频率
        if (isRequestToFrequest(loanActivityId, userId)) {
            return new BaseResponse<>(HttpStatus.OK, "请求频繁，请稍后再试", res);
        }

        // 校验验证吗
        //String cachedCodeKey = "" + userId + "_tryjoin_code";
        //String cachedCode = (String) redisService.get(cachedCodeKey);
        //if (cachedCode != null && varifyCode != null && !cachedCode.equals(varifyCode)) {
        //    return new BaseResponse<>(HttpStatus.BAD_REQUEST, "验证码错误", res);
        //}

        // 判断用户是否参加过活动
        String key = "MD5." + userId + "." + loanActivityId + ".JOIN_RESULT";
        String checkResultStr = stringRedisTemplate.opsForValue().get(key);
        // 获取商品ID

        LoanActivity loanActivity = loanActivityDao.findById(loanActivityId)
            .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        Long goodId = loanActivity.getGoodsId();
        res.setGoodId(goodId);

        // 获取随机字符串
        String random = stringRedisTemplate.opsForValue().get(ActivityTask.ACTIVITY_RANDOM_KEY + "." + goodId);
        res.setRandom(random);

        // 如果没有参加过,就走流程
        if (checkResultStr == null) {
            // 校验用户是否能通过初筛
            User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
            LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId())
                    .orElseThrow(() -> new DataRetrievalFailureException("该活动没有对应规则"));
            BaseResult<Boolean> baseResult = new LoanActivityService().checkUserInfo(loanActivity, loanRule, user);
            userLoanActivityDao.saveAndFlush(
                    UserLoanActivity.builder().user(user).loanActivity(loanActivity).isPassed(baseResult.getResult())
                            .build());
            if (!baseResult.getResult()) {
                stringRedisTemplate.opsForValue().set(key, "0");
                return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + baseResult.getMessage(), res);
            }
            // 缓存用户的筛选结果
            ArrayList<String> arrayList = new ArrayList<>();
            String time = String.valueOf(new Date().getTime());
            arrayList.add(AUTH_SALT);
            arrayList.add(String.valueOf(userId));
            arrayList.add(goodId.toString());
            arrayList.add(time);
            String md5 = MD5.md5(arrayList);
            res.setResult(true);
            res.setMd5(md5);
            stringRedisTemplate.opsForValue().set(key, "1");
            // MD5
            redisService.set(key + ".MD5", md5, 5);
            // TIMESTAMP
            stringRedisTemplate.opsForValue().set(USER_SEND_REQUEST_TIME_KEY + "." + + userId + "." + goodId, time);
            return new BaseResponse<>(HttpStatus.OK, "初筛通过, 参加成功", res);
        } else {
            res.setResult(checkResultStr.equals("1"));
            String md5 = (String) redisService.get(key + ".MD5");
            // 如果没拿到md5记录就重新生成
            if (md5 == null) {
                ArrayList<String> arrayList = new ArrayList<>();
                String time = String.valueOf(new Date().getTime());
                arrayList.add(AUTH_SALT);
                arrayList.add(String.valueOf(userId));
                arrayList.add(goodId.toString());
                arrayList.add(time);
                md5 = MD5.md5(arrayList);
                redisService.set(key, md5, 60 * 10);
                stringRedisTemplate.opsForValue().set(USER_SEND_REQUEST_TIME_KEY + "." + + userId + "." + goodId, time);
                res.setResult(true);
                res.setMd5(md5);
                stringRedisTemplate.opsForValue().set(key, "1");
                // MD5
                redisService.set(key + ".MD5", md5, 5);
                return new BaseResponse<>(HttpStatus.OK, "参加链接成功", res);
            }
            return new BaseResponse<>(HttpStatus.OK, "您已经参加过", res);
        }
    }

    public BaseResponse<LoanActivityResponse> findByIdFull(Long id) {
        LoanActivity loanActivity = loanActivityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", LoanActivityResponse.fromLoanActivity(loanActivity));
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