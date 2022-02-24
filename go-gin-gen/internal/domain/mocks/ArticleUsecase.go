package mocks

import (
	"go-gin-gen/internal/domain"

	"github.com/stretchr/testify/mock"
)

type ArticleUsecase struct {
	mock.Mock
}

func (_m *ArticleUsecase) GetByID(id uint) (domain.Article, error) {
	ret := _m.Called(id)

	var r0 domain.Article
	if rf, ok := ret.Get(0).(func(uint) domain.Article); ok {
		r0 = rf(id)
	} else {
		r0 = ret.Get(0).(domain.Article)
	}

	var r1 error
	if rf, ok := ret.Get(1).(func(uint) error); ok {
		r1 = rf(id)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1

}
