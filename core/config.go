package core

import (
	"fmt"
	"os"
	"strings"
)

func Load_dsn() error {
	file, err := os.ReadFile(".env")
	if err != nil {
		return fmt.Errorf(".env не найден")
	}

	dsn := strings.Split(string(file), "=")[1]
	os.Setenv("DSN", dsn)
	return nil
}
