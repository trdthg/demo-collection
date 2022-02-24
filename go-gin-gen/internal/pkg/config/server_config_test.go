package config

import "testing"

func TestServer(t *testing.T) {
	Server := (&server{}).Load("/home/trdthg/repo/trdthg-playground/go/go-gin-gen/conf/server.ini").Init()
	if Server == nil {
		t.Fail()
	}
}
