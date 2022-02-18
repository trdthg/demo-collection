package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.entity.User;
import com.moflowerlkh.decisionengine.enums.Employment;
import com.moflowerlkh.decisionengine.enums.EnumValue;
import com.moflowerlkh.decisionengine.enums.Gender;
import com.moflowerlkh.decisionengine.service.UserService;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;
import lombok.NonNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.Arrays;

@RestController
@Api(tags = {"用户相关"})
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    UserService userService;

    @PostMapping("/register")
    @ApiOperation("注册")
    public BaseResponse<Long> register(@RequestBody @Valid UserRequest userRequest) throws Exception {
        User user = userRequest.toUser();
        userService.register(user);
        return new BaseResponse<>(HttpStatus.CREATED, "成功", user.getId());
    }

    @GetMapping("/hello")
    @ApiOperation("打印hello xxx")
    public String hello(String username) {
        return "Hello" + username;
    }
}

@Data
class UserRequest {
    @NotBlank(message = "用户账号不能为空")
    @Size(min = 6, max = 11, message = "账号长度必须是6-11个字符")
    private String username;
    private String password;
    //user_name	string	姓名
    @NotBlank(message = "姓名不能为空")
    @Size(min = 6, max = 11, message = "姓名长度必须是1-50个字符")
    private String user_name;
    //user_gender	string	性别
    @NotBlank
    @EnumValue(enumClass=Gender.class, message = "性别类型不合法")
    private String user_gender;
    //user_IDnumber	string	身份证号
    private String user_IDnumber;
    //user_nation	string	国家
    private String user_nation;
    //user_age	number	年龄
    private Integer user_age;
    //user_overdual	number	近三年逾期还款次数
    private Long user_overdual;
    //user_employment	string	就业状态
    @EnumValue(enumClass=Employment.class, message = "就业类型不合法")
    private String user_employment;
    //user_dishonest	string	被列入失信人名单
    @NonNull
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

class UserResponse {
    private Long user_id;

    public static UserResponse fromUser(User user) {
        UserResponse userResponse = new UserResponse();
        userResponse.user_id = user.getId();
        return userResponse;
    }
}