package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	Host = "http://localhost:9200/"
	Type = "/line/"
)

type Worker interface {
	Task()
}

type Pool struct {
	work chan Worker
	wg   sync.WaitGroup
}

func New(maxGoroutines int) *Pool {
	p := Pool{
		work: make(chan Worker),
	}

	p.wg.Add(maxGoroutines)
	for i := 0; i < maxGoroutines; i++ {
		go func() {
			for w := range p.work {
				w.Task()
			}
			p.wg.Done()
		}()
	}

	return &p
}

func (p *Pool) Run(w Worker) {
	p.work <- w
}

func (p *Pool) Shutdown() {
	close(p.work)
	p.wg.Wait()
}

type lineUploader struct {
	text string
	id   int
}

type data struct {
	Text string `json:"text"`
}

func Put(url string, data io.Reader, contentType string) string {
	req, err := http.NewRequest(`PUT`, url, data)
	req.Header.Add(`content-type`, contentType)
	if err != nil {
		log.Println(err)
		return "error"
	}
	defer req.Body.Close()

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return "error"
	}
	defer resp.Body.Close()

	result, _ := ioutil.ReadAll(resp.Body)
	return string(result)
}

var wg sync.WaitGroup
var filename string
var fflag = flag.String("f", "", "filename")
var sflag = flag.Int("s", 0, "main goroutine sleep time")

func main() {
	flag.Parse()
	filename = *fflag
	if filename == "" {
		log.Fatal("Need Filename!")
	}

	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	defer func() {
		if err = f.Close(); err != nil {
			log.Fatal(err)
		}
	}()

	p := New(4096)

	buf := bufio.NewReader(f)
	for i := 1; i > 0; i++ {
		line, _, err := buf.ReadLine()

		wg.Add(1)
		lu := lineUploader{
			text: string(line),
			id:   i,
		}

		go func() {
			p.Run(&lu)
			wg.Done()
		}()

		if err != nil {
			fmt.Println(err)
			if err == io.EOF {
				break
			}
		}

		time.Sleep(time.Duration(*sflag) * time.Millisecond)
	}

	wg.Wait()
	p.Shutdown()
}

func (m *lineUploader) Task() {
	url := Host + strings.ToLower(filename) + Type + strconv.FormatInt(int64(m.id), 10)
	d := data{Text: m.text}
	if b, err := json.Marshal(d); err == nil {
		fmt.Println(Put(url, strings.NewReader(string(b)), "application/json"))
	} else {
		fmt.Println(err)
	}
}
