package usecase_test

import (
	"errors"
	"go-gin-gen/internal/domain"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"

	"go-gin-gen/api/article/usecase"
	"go-gin-gen/internal/domain/mocks"
)

func TestGetByID(t *testing.T) {
	mockArticleRepo := new(mocks.ArticleRepository)

	mockArticle := domain.Article{
		Name:  "the world",
		Title: "Hello",
	}

	t.Run("success", func(t *testing.T) {
		mockArticleRepo.On("GetByID", mock.AnythingOfType("uint")).Return(mockArticle, nil).Once()
		u := usecase.NewArticleUsecase(mockArticleRepo)
		a, err := u.GetByID(mockArticle.ID)
		assert.NoError(t, err)
		assert.NotNil(t, a)
		mockArticleRepo.AssertExpectations(t)
	})

	t.Run("error-failed", func(t *testing.T) {
		mockArticleRepo.On("GetByID", mock.AnythingOfType("uint")).Return(domain.Article{}, errors.New("Unexpected")).Once()
		u := usecase.NewArticleUsecase(mockArticleRepo)
		a, err := u.GetByID(mockArticle.ID)
		assert.Error(t, err)
		assert.Equal(t, domain.Article{}, a)
		mockArticleRepo.AssertExpectations(t)
	})
}
