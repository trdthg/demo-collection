package main

// 导入gin包
import (
	"fmt"
	articleDelivery "go-gin-gen/api/article/delivery/http"
	articleRepo "go-gin-gen/api/article/repo/mysql"
	articleUsecase "go-gin-gen/api/article/usecase"
	"go-gin-gen/internal/domain"
	"go-gin-gen/internal/pkg/config"

	"github.com/gin-gonic/gin"
	"go.uber.org/dig"
	"gorm.io/gorm"
)

type Router struct {
	method  string
	handler gin.HandlerFunc
}

func NewRouter(handler articleDelivery.ArticleHandler) map[string]Router {
	routers := make(map[string]Router)
	routers["/articles/:id"] = Router{method: "GET", handler: handler.GetByID}
	return routers
}

func BuildContainer() *dig.Container {
	container := dig.New()
	container.Provide(config.NewDB)
	container.Provide(articleRepo.NewArticleRepposity)
	container.Provide(articleUsecase.NewArticleUsecase)
	container.Provide(articleDelivery.NewArticleHandler)
	container.Provide(NewRouter)
	return container
}

// 入口函数
func main() {
	container := BuildContainer()
	r := gin.Default()
	conf := config.NewServerConfig()
	err := container.Invoke(func(routers map[string]Router, db *gorm.DB) {
		db.AutoMigrate(&domain.Article{})
		for key := range routers {
			r.Handle((routers)[key].method, key, (routers)[key].handler)
		}
		r.Run(fmt.Sprintf("%s:%d", conf.Address, conf.Port)) // 监听并在 0.0.0.0:8081 上启动服务
	})

	if err != nil {
		panic(err)
	}

}
