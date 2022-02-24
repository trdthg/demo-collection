package usecase

import "go-gin-gen/internal/domain"

type userUsecase struct {
	userRepo domain.UserRepo
}

func NewUserUsecase(r domain.UserRepo) domain.UserUsecase {
	return &userUsecase{
		userRepo: r,
	}
}

func (u *userUsecase) GetByID(id uint) (domain.User, error) {
	user, err := u.userRepo.GetByID(id)
	return user, err
}

func (u *userUsecase) Create(user *domain.User) error {
	err := u.userRepo.Create(user)
	return err
}
