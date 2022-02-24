package usecase_test

import (
	"errors"
	userUsecase "go-gin-gen/api/user/usecase"
	"go-gin-gen/internal/domain"
	"go-gin-gen/internal/domain/mocks"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestGetByID(t *testing.T) {
	mockUserRepo := new(mocks.UserRepo)
	mockUser := domain.User{
		Username: "ducker",
		Password: "aaaa",
	}
	t.Run("success", func(t *testing.T) {
		mockUserRepo.On("GetByID", mock.AnythingOfType("uint")).Return(mockUser, nil).Once()
		mockUseUsecase := userUsecase.NewUserUsecase(mockUserRepo)
		u, err := mockUseUsecase.GetByID(mockUser.ID)
		assert.NoError(t, err)
		assert.NotNil(t, u)
		mockUserRepo.AssertExpectations(t)
	})
	t.Run("failed", func(t *testing.T) {
		mockUserRepo.On("GetByID", mock.AnythingOfType("uint")).Return(domain.User{}, errors.New("Unexcepted")).Once()
		mockUseUsecase := userUsecase.NewUserUsecase(mockUserRepo)
		u, err := mockUseUsecase.GetByID(mockUser.ID)
		assert.Error(t, err)
		assert.Equal(t, domain.User{}, u)
		mockUserRepo.AssertExpectations(t)
	})
}

func TestCreate(t *testing.T) {

	mockUserRepo := new(mocks.UserRepo)
	mockUser := domain.User{
		Username: "ducker",
		Password: "aaaa",
	}
	t.Run("success", func(t *testing.T) {
		tempMockUser := mockUser
		tempMockUser.ID = 0
		mockUserRepo.On("GetByID", mock.AnythingOfType("uint")).Return(&domain.User{}).Once()
		mockUserRepo.On("Create", mock.AnythingOfType("*domain.User")).Return(nil).Once()
		mockUserUsecase := userUsecase.NewUserUsecase(mockUserRepo)
		err := mockUserUsecase.Create(&tempMockUser)
		assert.NoError(t, err)
		assert.Equal(t, mockUser.Username, tempMockUser.Username)
		mockUserRepo.AssertExpectations(t)
	})

	// t.Run("existing-username", func(t *testing.T) {
	// 	existingUser := mockUser
	// 	mockUserRepo.On("GetByUsername", mock.AnythingOfType("string")).Return(existingUser).Once()

	// 	mockArticleRepo.On("GetByTitle", mock.Anything, mock.AnythingOfType("string")).Return(existingArticle, nil).Once()
	// 	mockAuthor := domain.Author{
	// 		ID:   1,
	// 		Name: "Iman Tumorang",
	// 	}
	// 	mockAuthorrepo := new(mocks.AuthorRepository)
	// 	mockAuthorrepo.On("GetByID", mock.Anything, mock.AnythingOfType("int64")).Return(mockAuthor, nil)

	// 	u := ucase.NewArticleUsecase(mockArticleRepo, mockAuthorrepo, time.Second*2)

	// 	err := u.Store(context.TODO(), &mockArticle)

	// 	assert.Error(t, err)
	// 	mockArticleRepo.AssertExpectations(t)
	// 	mockAuthorrepo.AssertExpectations(t)
	// })
}
