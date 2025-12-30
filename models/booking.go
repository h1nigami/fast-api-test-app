package models

import "time"

type Booking struct {
	ID         int
	EventId    int
	CustomerID int
	Created_at time.Time
}
