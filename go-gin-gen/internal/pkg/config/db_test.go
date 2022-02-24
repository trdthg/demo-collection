package config

import (
	"testing"
)

func TestMysql(t *testing.T) {
	DB, err := (&database{}).Load("../../../config/db.ini").Init()
	if DB == nil || err != nil {
		t.Fail()
	}
}
