package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.domain.entities.Goods;
import com.moflowerlkh.decisionengine.domain.dao.GoodsDao;
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
@RequestMapping("/api/shoppinggoods")
public class GoodsController {

    @Autowired
    GoodsDao shoppingGoodsDao;

    @PostMapping("/")
    @ResponseBody
    @ApiOperation(value = "新增商品", notes = "新增一个商品")
    public BaseResponse<Goods> post(@RequestBody @Valid PostShoppingGoodsRequest request) {
        Goods shoppingGoods = request.toShoppingGoods();
        shoppingGoodsDao.save(shoppingGoods);
        return new BaseResponse<>(HttpStatus.CREATED, "新增商品成功", shoppingGoods);
    }

    @PutMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "编辑商品", notes = "根据 id 修改商品信息")
    public BaseResponse<Goods> put(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id,
            @RequestBody @Valid PostShoppingGoodsRequest request) {
        Goods shoppingGoods = request.toShoppingGoods();
        shoppingGoods.setId(id);
        shoppingGoodsDao.saveAndFlush(shoppingGoods);
        return new BaseResponse<>(HttpStatus.CREATED, "修改商品成功", shoppingGoods);
    }

    // @Timed(value = "查询商品", extraTags = { "url", "shoppinggoogs/get/id" })
    // @Counted(value = "查询商品", extraTags = { "url", "/shoppinggoogs/get{id}" })
    @GetMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "查询商品", notes = "根据 id 查找商品信息")
    public BaseResponse<Goods> put(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id) {
        Goods shoppingGoods = shoppingGoodsDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("查询结果为空，没有该商品"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", shoppingGoods);
    }

    @DeleteMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "删除商品", notes = "根据 id 删除商品")
    public BaseResponse<String> delete(
            @NotNull(message = "id 不能为空") @PositiveOrZero(message = "id 不能为负数") @PathVariable Long id) {
        shoppingGoodsDao.deleteById(id);
        return new BaseResponse<>(HttpStatus.OK, "删除成功", null);
    }
}

@Data
class PostShoppingGoodsRequest {

    @NotEmpty(message = "商品名不能为空")
    private String goods_name;

    private String goods_info;

    @NotNull(message = "商品总数不能为空")
    @PositiveOrZero(message = "商品总数只能是 0 或正整数")
    private Long goods_total;

    public Goods toShoppingGoods() {
        Goods shoppingGoods = new Goods();
        shoppingGoods.setCreateDate(new Date());
        shoppingGoods.setOneMaxAmount(1);
        shoppingGoods.setGoodsAmount(goods_total);
        return shoppingGoods;
    }
}