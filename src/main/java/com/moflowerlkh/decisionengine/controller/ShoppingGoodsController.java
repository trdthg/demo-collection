package com.moflowerlkh.decisionengine.controller;

import com.moflowerlkh.decisionengine.dao.ShoppingGoodsDao;
import com.moflowerlkh.decisionengine.entity.ShoppingGoods;
import com.moflowerlkh.decisionengine.vo.BaseResponse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataRetrievalFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@RestController
@Api(tags = { "商品相关" })
@RequestMapping("/api/shoppinggoods")
public class ShoppingGoodsController {

    @Autowired
    ShoppingGoodsDao shoppingGoodsDao;

    @PostMapping("/")
    @ResponseBody
    @ApiOperation(value = "新增商品", notes = "新增一个商品")
    public BaseResponse<ShoppingGoods> post(@RequestBody @Valid PostShoppingGoodsRequest request) {
        ShoppingGoods shoppingGoods = request.toShoppingGoods();
        shoppingGoodsDao.save(shoppingGoods);
        return new BaseResponse<>(HttpStatus.CREATED, "新增商品成功", shoppingGoods);
    }

    @PutMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "编辑商品", notes = "根据id修改商品信息")
    public BaseResponse<ShoppingGoods> put(
            @NotNull(message = "id不能为空") @PositiveOrZero(message = "id不能为负数") @PathVariable Long id,
            @RequestBody @Valid PostShoppingGoodsRequest request) {
        ShoppingGoods shoppingGoods = request.toShoppingGoods();
        shoppingGoods.setId(id);
        shoppingGoodsDao.saveAndFlush(shoppingGoods);
        return new BaseResponse<>(HttpStatus.CREATED, "修改商品成功", shoppingGoods);
    }

    @GetMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "查询商品", notes = "根据id查找商品信息")
    public BaseResponse<ShoppingGoods> put(
            @NotNull(message = "id不能为空") @PositiveOrZero(message = "id不能为负数") @PathVariable Long id) {
        ShoppingGoods shoppingGoods = shoppingGoodsDao.findById(id)
                .orElseThrow(() -> new DataRetrievalFailureException("查询结果为空，没有该商品"));
        return new BaseResponse<>(HttpStatus.OK, "查询成功", shoppingGoods);
    }

    @DeleteMapping("/{id}")
    @ResponseBody
    @ApiOperation(value = "删除商品", notes = "根据id删除商品")
    public BaseResponse<String> delete(
            @NotNull(message = "id不能为空") @PositiveOrZero(message = "id不能为负数") @PathVariable Long id) {
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
    @PositiveOrZero(message = "商品总数只能是0或正整数")
    private Long goods_total;

    public ShoppingGoods toShoppingGoods() {
        ShoppingGoods shoppingGoods = new ShoppingGoods();
        shoppingGoods.setName(goods_name);
        shoppingGoods.setInfo(goods_info);
        shoppingGoods.setGoodsTotal(goods_total);
        return shoppingGoods;
    }
}