package mysql_test

import (
	"testing"
	"time"

	userRepo "go-gin-gen/api/user/repo/mysql"

	"github.com/stretchr/testify/assert"
	"gopkg.in/DATA-DOG/go-sqlmock.v1"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func TestGetByID(t *testing.T) {
	// 准备加数据库 准备加数据，准备模拟的SQL和执行结果
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

	rows := sqlmock.NewRows([]string{"id", "username", "password", "deleted_at", "updated_at", "created_at"}).
		AddRow(1, "name 1", "title 1", nil, time.Now(), time.Now())
	query := "SELECT * FROM user WHERE ID = \\?"
	mock.ExpectQuery(query).WillReturnRows(rows)
	a := userRepo.NewUserRepo(gdb)
	anArticle, err := a.GetByID(1)
	assert.NoError(t, err)
	assert.NotNil(t, anArticle)
}

func TestGetByUsername(t *testing.T) {
	// 准备加数据库 准备加数据，准备模拟的SQL和执行结果
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
	rows := sqlmock.NewRows([]string{"id", "username", "password", "deleted_at", "updated_at", "created_at"}).
		AddRow(1, "name 1", "title 1", nil, time.Now(), time.Now())
	query := "SELECT * FROM user WHERE username = \\?"
	mock.ExpectQuery(query).WillReturnRows(rows)
	a := userRepo.NewUserRepo(gdb)
	anArticle, err := a.GetByUsername("name 1")
	assert.NoError(t, err)
	assert.NotNil(t, anArticle)
}
