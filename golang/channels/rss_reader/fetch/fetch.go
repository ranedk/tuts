package fetch

import (
	"github.com/SlyMarbo/rss"
)

type Fetcher interface {
	Fetch() ([]*rss.Item, error)
}

func Fetch(url string) Fetcher {
	rssReader := RssReader{url: url}
	return rssReader
}
