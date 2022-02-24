package usecase

import "go-gin-gen/internal/domain"

type articleUsecase struct {
	articleRepo domain.ArticleRepo
}

func NewArticleUsecase(a domain.ArticleRepo) domain.ArticleUsecase {
	return &articleUsecase{
		articleRepo: a,
	}
}

func (a *articleUsecase) GetByID(id uint) (res domain.Article, err error) {
	res, err = a.articleRepo.GetByID(id)
	if err != nil {
		return
	}
	return
}
