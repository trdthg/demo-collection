package domain

import "gorm.io/gorm"

type Article struct {
	gorm.Model
	Name  string
	Title string
}

type ArticleRepo interface {
	GetByID(id uint) (Article, error)
}

type ArticleUsecase interface {
	GetByID(id uint) (Article, error)
}
