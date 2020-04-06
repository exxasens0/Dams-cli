package http

import (
	"encoding/json"
	"fmt"
	damscli "github.com/exxasens0/Dams-cli/internal"
	"io/ioutil"
	"net/http"
	_ "strings"
)

const (
	productsEndpoint = "/sdim2/apirest/catalog?componentType=embassament"
	URL              = "http://aca-web.gencat.cat"
)

// DamsRepo definiton of methods to access a data
type DamsRepo interface {
	JSONToStructDamData() ([]damscli.Dam, error)
}

type damsRepo struct {
	url string
}

func NewDamRepositoryFromHttp() DamsRepo {
	return &damsRepo{url: URL}
}

//Get all dam Data
func (b *damsRepo) JSONToStructDamData() (dams []damscli.Dam, err error) {
	response, err := http.Get(fmt.Sprintf("%v%v", b.url, productsEndpoint))
	if err != nil {
		fmt.Println(">> ", err)
		return nil, err
	}
	contents, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Println(">> ", err)
		return nil, err
	}

	//response body without [ at begining and  ] at end, json can't unmarshall it without square brackets
	//add these symbols to body response
	contents = insertByte(contents, 0, 91) //Insert "[" at firs position
	contents = append(contents, 93)        //Insert "]" at last position

	err = json.Unmarshal(contents, &dams)
	if err != nil {
		fmt.Println(">> ", err)
		return nil, err
	}

	return
}

func insertByte(array []byte, index int, value byte) []byte {
	return append(array[:index], append([]byte{value}, array[index:]...)...)
}
