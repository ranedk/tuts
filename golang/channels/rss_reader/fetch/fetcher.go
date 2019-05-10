package fetch

import "fmt"

import (
	"github.com/SlyMarbo/rss"
)

type RssReader struct {
	url string
}

func (rssReader RssReader) Fetch() ([]*rss.Item, error) {
	feed, err := rss.Fetch(rssReader.url)
	if err != nil {
		fmt.Println("Error fetching: ", err)
		return nil, err
	}
	return feed.Items, nil
}
