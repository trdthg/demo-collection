package helper

import (
	"fmt"
	"testing"
)

func TestPathExist(t *testing.T) {
	path := "../../../config/db.ini"
	// path := "path_util_test.go"
	fmt.Println(path)
	exist, err := PathExists(path)
	if exist == false || err != nil {
		t.Fail()
	}
}
