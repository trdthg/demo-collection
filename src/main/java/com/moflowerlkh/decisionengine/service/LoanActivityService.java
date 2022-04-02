package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.entities.UserLoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.activities.LoanActivity;
import com.moflowerlkh.decisionengine.domain.entities.rules.LoanRule;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.LoanActivityResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.LoanActivitySimpleResponse;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.SetLoanActivityRequest;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.SetLoanActivityRuleRequest;
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
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import javax.validation.Valid;
import java.util.List;
import java.util.Objects;
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
        loanActivityDao.save(loanActivity);
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
    public BaseResult<Boolean> checkUserInfo(LoanActivity loanActivity, User user) {
        BaseResult<Boolean> baseResult = new BaseResult<>();
        baseResult.setResult(false);
        LoanRule loanRule = loanRuleDao.findById(loanActivity.getLoanRuleId())
                .orElseThrow(() -> new DataRetrievalFailureException("查询活动规则失败"));
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

    @Timed("写入数据库耗时")
    @Counted("写入数据库频率")
    public BaseResponse<Boolean> tryJoin(Long loanActivityId, Long userId) {
        LoanActivity loanActivity = loanActivityDao.findById(loanActivityId)
                .orElseThrow(() -> new DataRetrievalFailureException("没有该活动"));
        User user = userDao.findById(userId).orElseThrow(() -> new DataRetrievalFailureException("没有该用户"));
        UserLoanActivity userLoanActivity = userLoanActivityDao.findByUserAndLoanActivity(user, loanActivity);
        if (userLoanActivity == null) {
            BaseResult<Boolean> baseResult = new LoanActivityService().checkUserInfo(loanActivity, user);
            userLoanActivityDao.saveAndFlush(
                    UserLoanActivity.builder().user(user).loanActivity(loanActivity).isPassed(baseResult.getResult())
                            .build());
            if (baseResult.getResult()) {
                return new BaseResponse<>(HttpStatus.OK, "初筛通过, 参加成功", true);
            } else {
                return new BaseResponse<>(HttpStatus.OK, "初筛不通过: " + baseResult.getMessage(), false);
            }
        } else {
            return new BaseResponse<>(HttpStatus.OK, "您已经参加过", userLoanActivity.getIsPassed());
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
}
