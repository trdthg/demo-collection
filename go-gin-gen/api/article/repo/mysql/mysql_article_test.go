package mysql_test

import (
	"regexp"
	"testing"
	"time"

	"gorm.io/driver/mysql"

	"github.com/stretchr/testify/assert"
	"gopkg.in/DATA-DOG/go-sqlmock.v1"
	"gorm.io/gorm"

	articleRepo "go-gin-gen/api/article/repo/mysql"
)

func TestGetByID(t *testing.T) {

	db, mock, err := sqlmock.New()
	if err != nil {
		panic("sqlmock new error!")
	}

	gdb, err := gorm.Open(mysql.New(mysql.Config{
		Conn:                      db,
		SkipInitializeWithVersion: true,
	}), &gorm.Config{})

	if err != nil {
		t.Fatalf("an error '%s' was not expected when opening a stub database connection", err)
	}

	rows := sqlmock.NewRows([]string{"id", "name", "title", "deleted_at", "updated_at", "created_at"}).
		AddRow(1, "name 1", "title 1", nil, time.Now(), time.Now())

	query := "SELECT id, name, title, deleted_at, updated_at, created_at FROM article WHERE ID = ?"

	mock.ExpectQuery(regexp.QuoteMeta(query)).WillReturnRows(rows)

	a := articleRepo.NewArticleRepposity(gdb)

	anArticle, err := a.GetByID(1)

	assert.NoError(t, err)
	assert.NotNil(t, anArticle)
}
