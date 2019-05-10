package main

import (
	"fmt"
)

import (
	"rss_reader/fetch"
)

func main() {

	RssUris := [...]string{
		"https://www.technologyreview.com/topnews.rss",
		"https://readwrite.com/feed/?x=1",
		"http://feeds.arstechnica.com/arstechnica/technology-lab",
		"http://feeds.feedburner.com/TechCrunch",
		"http://www.recode.net/rss/index.xml",
		"http://blogs.barrons.com/techtraderdaily/feed/",
	}

	rssReader := &fetch.RssReader{url: RssUris[0]}
	items, _ := rssReader.Fetch()
	fmt.Println("Feed> ", items)
}
