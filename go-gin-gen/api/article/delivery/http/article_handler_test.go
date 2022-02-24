package http_test

import (
	"go-gin-gen/internal/domain"
	"go-gin-gen/internal/domain/mocks"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"

	articleHttp "go-gin-gen/api/article/delivery/http"

	"github.com/bxcodec/faker"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestGetByID(t *testing.T) {
	// 准备加数据，让调用usecase是必定返回假数据
	var mockArticle domain.Article
	err := faker.FakeData(&mockArticle)
	assert.NoError(t, err)
	mockArticleUsecase := new(mocks.ArticleUsecase)
	mockArticleUsecase.On("GetByID", mock.AnythingOfType("uint")).Return(mockArticle, nil)
	mockArticleHandler := articleHttp.ArticleHandler{
		ArticleUsecase: mockArticleUsecase,
	}

	gin.SetMode(gin.TestMode)
	r := gin.Default()
	r.GET("/article/:id", mockArticleHandler.GetByID)

	num := int(mockArticle.ID)
	req, err := http.NewRequest(http.MethodGet, "/article/"+strconv.Itoa(num), nil)
	if err != nil {
		t.Fatalf("Couldn't create request: %v\n", err)
	}

	// Create a response recorder so you can inspect the response
	w := httptest.NewRecorder()

	// Perform the request
	r.ServeHTTP(w, req)

	// Check to see if the response was what you expected
	if w.Code != http.StatusOK {
		t.Fatalf("Expected to get status %d but instead got %d\n", http.StatusOK, w.Code)
	}
}
