package config

import (
	"go-gin-gen/internal/pkg/helper"

	"gopkg.in/ini.v1"
)

type server struct {
	Address string
	Port    int
	source  *ini.File
}

func (s *server) Load(path string) *server {
	var err error
	//判断配置文件是否存在
	exists, err := helper.PathExists(path)
	if !exists || err != nil {
		return s
	}
	s.source, err = ini.Load(path)
	if err != nil {
		panic(err)
	}
	return s
}

func (s *server) Init() *server {
	//判断配置是否加载成功
	if s.source == nil {
		return s
	}
	s.Address = s.source.Section("server").Key("address").MustString("0.0.0.0")
	s.Port = s.source.Section("server").Key("port").MustInt(8081)
	return s
}

func NewServerConfig() *server {
	return (&server{}).Load("config/server.ini").Init()
}
