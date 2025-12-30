package core

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v4"
)

var db *pgx.Conn

func InitDatabase(ctx context.Context, db_url string) error {
	var err error
	db, err = pgx.Connect(ctx, db_url)
	if err != nil {
		panic(err.Error())
	}

	if err := db.Ping(ctx); err != nil {
		return fmt.Errorf("failed to ping database")
	}
	return nil
}

func Getdb() *pgx.Conn {
	return db
}
