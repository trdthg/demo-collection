package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.domain.entities.Commodity;
import com.moflowerlkh.decisionengine.domain.dao.CommodityDao;
import com.moflowerlkh.decisionengine.vo.BaseResponse;

//import io.micrometer.core.annotation.Counted;
//import io.micrometer.core.annotation.Timed;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.Date;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@RestController
@Api(tags = { "商品相关" })
@RequestMapping("/api/commodity")
public class CommodityController {

    @Autowired
    CommodityDao commodityDao;

    @PostMapping("/")
    @ResponseBody
    @ApiOperation(value = "新增商品", notes = "新增一个商品")
    public BaseResponse<Commodity> post(@RequestBody @Valid PostCommodityRequest request) {
        Commodity commodity = request.into();
        commodityDao.save(commodity);
        return new BaseResponse<>(HttpStatus.CREATED, "新增商品成功", commodity);
    }

    @PutMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "编辑商品", notes = "根据 id 修改商品信息")
    public BaseResponse<Commodity> put(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id,
            @RequestBody @Valid PostCommodityRequest request) {
        Commodity commodity = request.into();
        commodity.setId(id);
        commodityDao.saveAndFlush(commodity);
        return new BaseResponse<>(HttpStatus.CREATED, "修改商品成功", commodity);
    }

    @GetMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "查询商品", notes = "根据 id 查找商品信息")
    public BaseResponse<Commodity> put(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id) {
        Commodity Commodity = commodityDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("查询结果为空，没有该商品"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", Commodity);
    }

    @DeleteMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "删除商品", notes = "根据 id 删除商品")
    public BaseResponse<String> delete(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id) {
        commodityDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", null);
    }
}

@Data
class PostCommodityRequest {

    @NotEmpty(message = "商品名不能为空")
    private String name;

    private String info;

    @NotNull(message = "商品总数不能为空")
    @PositiveOrZero(message = "商品总数只能是 0 或正整数")
    private Long amount;

    @NotNull(message = "商品价格不能为空")
    @PositiveOrZero(message = "商品价格只能是 0 或正整数")
    private Long price;

    public Commodity into() {
        Commodity commodity = new Commodity();
        commodity.setCreateDate(new Date());
        commodity.setName(name);
        commodity.setName(info);
        commodity.setPrice(price);
        commodity.setAmount(amount);
        return commodity;
    }
}