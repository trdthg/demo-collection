package mysql

import (
	"go-gin-gen/internal/domain"

	"gorm.io/gorm"
)

type mysqlArticleRepo struct {
	Conn *gorm.DB
}

func NewArticleRepposity(Conn *gorm.DB) domain.ArticleRepo {
	return &mysqlArticleRepo{Conn}
}

func (m *mysqlArticleRepo) GetByID(id uint) (domain.Article, error) {
	article := domain.Article{}
	m.Conn.First(&article, 1)
	return article, nil
}
