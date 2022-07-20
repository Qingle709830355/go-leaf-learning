package utils

import (
	"github.com/name5566/leaf/log"
	"path/filepath"
)

func getCurrentAbPath() string {
	filename, err := filepath.Abs("")
	if err != nil {
		log.Fatal("%v", err)
	}
	return filename
}

var (
	BASE_PATH = getCurrentAbPath()
	BIN_PATH  = filepath.Join(BASE_PATH, "bin")
	//SRC_PATH  = filepath.Join(BASE_PATH, "src")
)
