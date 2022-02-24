package mysql

import (
	"go-gin-gen/internal/domain"

	"gorm.io/gorm"
)

type userRepo struct {
	DB *gorm.DB
}

func NewUserRepo(db *gorm.DB) domain.UserRepo {
	return &userRepo{
		DB: db,
	}
}

func (a *userRepo) GetByID(id uint) (domain.User, error) {
	u := domain.User{}
	res := a.DB.First(&u, id)
	return u, res.Error
}

func (a *userRepo) GetByUsername(username string) (domain.User, error) {
	u := domain.User{}
	res := a.DB.Where("username = \\?", username).First(&u)
	return u, res.Error
}

func (a *userRepo) Create(u *domain.User) error {
	res := a.DB.Create(u)
	return res.Error
}
