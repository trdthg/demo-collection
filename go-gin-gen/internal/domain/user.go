package domain

import "gorm.io/gorm"

type User struct {
	gorm.Model
	Username string
	Password string
}

type UserRepo interface {
	GetByID(id uint) (User, error)
	GetByUsername(username string) (User, error)
	Create(u *User) error
}

type UserUsecase interface {
	GetByID(id uint) (User, error)
	GetByUsername(username string) (User, error)
	Create(u *User) error
}
