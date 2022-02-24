package config

import (
	"errors"
	"fmt"
	"go-gin-gen/internal/pkg/helper"

	"gopkg.in/ini.v1"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type database struct {
	Host     string `ini:"host"`
	Port     int    `ini:"port"`
	Database string `ini:"database"`
	Username string `ini:"username"`
	Password string `ini:"password"`

	source *ini.File
}

func (d *database) Load(path string) *database {
	fmt.Println("is exists: ")
	var err error

	exists, err := helper.PathExists(path)
	fmt.Println(exists)
	if !exists {
		return d
	}
	d.source, err = ini.Load(path)
	if err != nil {
		panic(err)
	}

	return d
}

func (d *database) Init() (*gorm.DB, error) {
	if d.source == nil {
		panic(errors.New("database.source is nil"))
	}
	d.Host = d.source.Section("mysql").Key("host").MustString("127.0.0.1")
	d.Port = d.source.Section("mysql").Key("port").MustInt(3306)
	d.Database = d.source.Section("mysql").Key("database").MustString("dev")
	d.Username = d.source.Section("mysql").Key("username").MustString("root")
	d.Password = d.source.Section("mysql").Key("password").MustString("000000")

	dsn := fmt.Sprintf("%v:%v@tcp(%v:%v)/%v?charset=utf8mb4&parseTime=True&loc=Local",
		d.Username,
		d.Password,
		d.Host,
		d.Port,
		d.Database,
	)
	DB, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
		DisableForeignKeyConstraintWhenMigrating: true,
	})
	if err != nil {
		panic(err)
	}

	return DB, nil
}

func NewDB() *gorm.DB {
	DB, err := (&database{}).Load("config/db.ini").Init()
	if err != nil {
		panic("connect to db failed")
	}

	return DB
}
