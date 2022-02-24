package http

import (
	"go-gin-gen/internal/domain"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

type ArticleHandler struct {
	ArticleUsecase domain.ArticleUsecase
}

func NewArticleHandler(a domain.ArticleUsecase) ArticleHandler {
	handler := ArticleHandler{
		ArticleUsecase: a,
	}
	return handler
}

func (a *ArticleHandler) GetByID(c *gin.Context) {

	idP, err := strconv.Atoi(c.Param("id"))

	if err != nil {
		c.JSON(http.StatusNotFound, domain.ErrNotFound.Error())
		return
	}

	id := uint(idP)

	art, err := a.ArticleUsecase.GetByID(id)
	if err != nil {
		c.JSON(getStatusCode(err), gin.H{"Message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, art)
}

func getStatusCode(err error) int {
	if err == nil {
		return http.StatusOK
	}

	logrus.Error(err)
	switch err {
	case domain.ErrInternalServerError:
		return http.StatusInternalServerError
	case domain.ErrNotFound:
		return http.StatusNotFound
	case domain.ErrConflict:
		return http.StatusConflict
	default:
		return http.StatusInternalServerError
	}
}
