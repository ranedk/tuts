package subscribe

import "github.com/SlyMarbo/rss"

type Subscription interface {
	Updates() <-chan rss.Item
	Close() error
}

//func Subscribe(fetcher Fetcher) Subscription {
//}
