package mocks

import (
	"go-gin-gen/internal/domain"

	"github.com/stretchr/testify/mock"
)

type UserRepo struct {
	mock.Mock
}

func (m *UserRepo) GetByID(id uint) (domain.User, error) {
	args := m.Called(id)
	var r0 domain.User
	if rf, ok := args.Get(0).(func(uint) domain.User); ok {
		r0 = rf(id)
	} else {
		r0 = args.Get(0).(domain.User)
	}

	var r1 error
	if rf, ok := args.Get(1).(func(uint) error); ok {
		r1 = rf(id)
	} else {
		r1 = args.Error(1)
	}
	return r0, r1
}

func (m *UserRepo) GetByUsername(username string) (domain.User, error) {
	args := m.Called(username)
	var r0 domain.User
	if rf, ok := args.Get(0).(func(string) domain.User); ok {
		r0 = rf(username)
	} else {
		r0 = args.Get(0).(domain.User)
	}

	var r1 error
	if rf, ok := args.Get(1).(func(string) error); ok {
		r1 = rf(username)
	} else {
		r1 = args.Error(1)
	}
	return r0, r1
}

func (_m *UserRepo) Create(user *domain.User) error {
	ret := _m.Called(user)
	var r0 error
	if rf, ok := ret.Get(0).(func(*domain.User) error); ok {
		r0 = rf(user)
	} else {
		r0 = ret.Error(0)
	}
	return r0
}
