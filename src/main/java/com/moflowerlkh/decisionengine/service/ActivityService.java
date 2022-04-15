package com.moflowerlkh.decisionengine.service;

import com.moflowerlkh.decisionengine.domain.dao.*;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.domain.entities.UserActivity;
import com.moflowerlkh.decisionengine.service.LoanActivityServiceDTO.JoinLoanActivityUserResponseDTO;
import com.moflowerlkh.decisionengine.util.CodeResult;
import com.moflowerlkh.decisionengine.util.ValidateCode;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Service
public class ActivityService {
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

    public BaseResponse<List<JoinLoanActivityUserResponseDTO>> getPassedUsers(Long activity_id) {
        List<UserActivity> userActivities = userActivityDao.findByActivityId(activity_id);
        List<JoinLoanActivityUserResponseDTO> res = userActivities.stream().filter(UserActivity::getIsPassed).map(x -> {
            User user = userDao.getById(x.getUserId());
            return JoinLoanActivityUserResponseDTO.fromUser(user);
        }).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }

    public BaseResponse<List<JoinLoanActivityUserResponseDTO>> getUnPassedUsers(Long activity_id) {
        List<UserActivity> userActivities = userActivityDao.findByActivityId(activity_id);
        List<JoinLoanActivityUserResponseDTO> res = userActivities.stream().filter(x -> !x.getIsPassed()).map(x -> {
            User user = userDao.getById(x.getUserId());
            return JoinLoanActivityUserResponseDTO.fromUser(user);
        }).collect(Collectors.toList());
        return new BaseResponse<>(HttpStatus.OK, "查询成功", res);
    }

    public BaseResponse<JoinLoanActivityUserResponseDTO> getPassedUser(Long activity_id, String name) {
        User user = userDao.findByUsername(name);
        if (user == null) {
            return new BaseResponse<>(HttpStatus.BAD_REQUEST, "查询失败: 没有该用户", null);
        }
        List<UserActivity> userActivities = userActivityDao.findByActivityId(activity_id);
        for (UserActivity x : userActivities) {
            if (Objects.equals(x.getUserId(), user.getId()) && x.getIsPassed()) {
                return new BaseResponse<>(HttpStatus.OK, "查询成功", JoinLoanActivityUserResponseDTO.fromUser(user));
            }
        }
        return new BaseResponse<>(HttpStatus.OK, "查询失败", null);
    }

    public BaseResponse<JoinLoanActivityUserResponseDTO> getUnpassedUser(Long activity_id, String name) {
        User user = userDao.findByUsername(name);
        List<UserActivity> userActivities = userActivityDao.findByActivityId(activity_id);
        for (UserActivity x : userActivities) {
            if (Objects.equals(x.getUserId(), user.getId()) && !x.getIsPassed()) {
                return new BaseResponse<>(HttpStatus.OK, "查询成功", JoinLoanActivityUserResponseDTO.fromUser(user));
            }
        }
        return new BaseResponse<>(HttpStatus.OK, "查询失败", null);
    }

    public BaseResponse<String> generateCaptchaBase64() {
        UsernamePasswordAuthenticationToken authenticationToken = (UsernamePasswordAuthenticationToken) SecurityContextHolder
            .getContext().getAuthentication();
        LoginUser loginUser = (LoginUser) authenticationToken.getPrincipal();
        Long userid = loginUser.getId();
        CodeResult codeResult = ValidateCode.getRandomCodeBase64();
        String key = "" + userid + "_tryjoin_code";
        redisService.set(key, codeResult.getRendom_string(), 60);
        String url = "data:image/png;base64," + codeResult.getBase64String();
        return new BaseResponse<>(HttpStatus.OK, "验证吗图片获取成功", url);
    }

}
