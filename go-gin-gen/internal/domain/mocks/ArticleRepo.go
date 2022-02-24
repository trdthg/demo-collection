package mocks

import (
	"go-gin-gen/internal/domain"

	"github.com/stretchr/testify/mock"
)

type ArticleRepository struct {
	mock.Mock
}

func (m *ArticleRepository) GetByID(id uint) (domain.Article, error) {
	args := m.Called(id)
	var r0 domain.Article
	if rf, ok := args.Get(0).(func(uint) domain.Article); ok {
		r0 = rf(id)
	} else {
		r0 = args.Get(0).(domain.Article)
	}

	var r1 error
	if rf, ok := args.Get(1).(func(uint) error); ok {
		r1 = rf(id)
	} else {
		r1 = args.Error(1)
	}
	return r0, r1
}
