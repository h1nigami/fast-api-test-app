package main

import (
	"context"
	"go-api-test-app/core"
	"os"
)

func main() {
	//example dsn = "postgres://postgres:postgres@localhost:5432/postgres"
	if err := core.InitDatabase(context.Background(), os.Getenv("DSN")); err != nil {
		panic(err)
	}
}
