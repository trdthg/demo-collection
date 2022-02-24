package api

import (
	"go-gin-gen/internal/validator"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Test(c *gin.Context) {
	//实例化一个TestRequest结构体，用于接收参数
	testStruct := validator.TestRequest{}

	//接收请求参数
	err := c.ShouldBind(&testStruct)

	//判断参数校验是否通过，如果不通过，把错误返回给前端
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"error": validator.Translate(err)})
		return
	}

	//校验通过，返回请求参数
	c.JSON(http.StatusOK, gin.H{"params": testStruct})
}
