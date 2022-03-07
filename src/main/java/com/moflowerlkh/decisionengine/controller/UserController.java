package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.dao.UserDao;
import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.EnumValue;
import com.moflowerlkh.decisionengine.enums.Gender;
import com.moflowerlkh.decisionengine.service.LoanService;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import com.moflowerlkh.decisionengine.vo.BaseResult;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;
import lombok.NonNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@RestController
@Api(tags = {"用户相关"})
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    LoanService loanService;
    @Autowired
    UserDao userDao;

    @PostMapping("/")
    @ApiOperation("注册")
    public BaseResponse<UserResponse> register(@RequestBody @Valid UserRequest userRequest) throws Exception {
        User user = userRequest.toUser();
        userDao.save(user);
        return new BaseResponse<>(HttpStatus.CREATED, "注册成功", UserResponse.fromUser(user));
    }

    @GetMapping("/{id}")
    @ApiOperation("根据id获取用户信息")
    public BaseResponse<UserResponse> get(@Valid @NotNull @PathVariable Long id) throws Exception {
        User user = userDao.findById(id).orElseThrow(() -> new DataRetrievalFailureException("没有该用户: id = " + id));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", UserResponse.fromUser(user));
    }

    @PutMapping("/{id}")
    @ApiOperation("根据id编辑用户信息")
    public BaseResponse<UserResponse> put(@Valid @PathVariable Long id, @RequestBody @Valid UserRequest userRequest) throws Exception {
        User user = userRequest.toUser();
        user.setId(id);
        userDao.saveAndFlush(user);
        return new BaseResponse<>(HttpStatus.CREATED, "编辑成功", UserResponse.fromUser(user));
    }

    @PostMapping("/{id}")
    @ApiOperation("根据id删除用户")
    public BaseResponse<Void> felete(@Valid @PathVariable Long id) throws Exception {
        userDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", null);
    }

    @GetMapping("/{user_id}/join/{activity_id}/")
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
class UserRequest {
    @NotBlank(message = "用户账号不能为空")
    @Size(min = 6, max = 11, message = "账号长度必须是6-11个字符")
    private String username;
    @NotBlank(message = "用户密码不能为空")
    private String password;
    //user_name	string	姓名
    @NotBlank(message = "姓名不能为空")
    @Size(min = 6, max = 11, message = "姓名长度必须是1-50个字符")
    private String user_name;
    //user_gender	string	性别
    @NotBlank
    @EnumValue(enumClass=Gender.class, message = "性别类型只能是[Male, Female]")
    private String user_gender;
    //user_IDnumber	string	身份证号
    @NotBlank(message = "身份证号不能为空")
    private String user_IDnumber;
    //user_nation	string	国家
    @NotBlank(message = "国籍不能为空")
    private String user_nation;
    //user_age	number	年龄
    @NotBlank(message = "年龄不能为空")
    private Integer user_age;
    //user_overdual	number	近三年逾期还款次数
    @NotBlank(message = "近三年逾期还款次数不能为空")
    private Long user_overdual;
    //user_employment	string	就业状态
    @NotBlank(message = "就业状态不能为空")
    @EnumValue(enumClass=Employment.class, message = "就业类型不合法: [Employed, Unemployed, Retired, Other, ..]")
    private String user_employment;
    //user_dishonest	string	被列入失信人名单
    @NonNull
    @NotBlank(message = "是否被列入失信人名单不能为空")
    private Boolean user_dishonest;

    public User toUser() {
        User user = new User();
        // 枚举
        Employment employment = Employment.valueOf(user_employment);
        user.setEmployment(employment);
        Gender gender = Gender.valueOf(user_gender);
        user.setGender(gender);

        // 用户名密码
        String encodedPassword = new BCryptPasswordEncoder().encode(password);
        user.setPassword(encodedPassword);
        user.setUsername(username);

        // 普通
        user.setName(user_name);
        user.setIDNumber(user_IDnumber);
        user.setCountry(user_nation);
        user.setAge(user_age);
        user.setOverDual(user_overdual);
        user.setDishonest(user_dishonest);
        return user;
    }
}

@Data
class UserResponse {
    private Long user_id;
    private String username;
    private String user_name;
    private String user_gender;
    private String user_IDnumber;
    private String user_nation;
    private Integer user_age;
    private Long user_overdual;
    private String user_employment;
    private Boolean user_dishonest;

    public static UserResponse fromUser(User user) {
        UserResponse userResponse = new UserResponse();
        userResponse.setUser_id(user.getId());
        userResponse.setUser_name(user.getName());
        userResponse.setUsername(user.getUsername());
        userResponse.setUser_gender(user.getGender().toString());
        userResponse.setUser_IDnumber(user.getIDNumber());
        userResponse.setUser_nation(user.getCountry());
        userResponse.setUser_age(user.getAge());
        userResponse.setUser_overdual(user.getOverDual());
        userResponse.setUser_employment(user.getEmployment().toString());
        userResponse.setUser_dishonest(user.getDishonest());
        userResponse.user_id = user.getId();
        return userResponse;
    }
}