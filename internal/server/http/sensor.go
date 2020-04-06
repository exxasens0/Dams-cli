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
	sensorValueEndPoint = "/sdim2/apirest/data/EMBASSAMENT-EST"
	damsURL             = "http://aca-web.gencat.cat"
)

// DamsRepo definiton of methods to access a data
type SensorRepo interface {
	JSONToStructSensorData() ([]damscli.SensorValue, error)
}

type sensorRepo struct {
	url string
}

func NewSensorepositoryFromHttp() SensorRepo {
	return &sensorRepo{url: damsURL}
}

func (s *sensorRepo) JSONToStructSensorData() (sensorvalues []damscli.SensorValue, err error) {
	response, err := http.Get(fmt.Sprintf("%v%v", s.url, sensorValueEndPoint))

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

	err = json.Unmarshal(contents, &sensorvalues)
	if err != nil {
		fmt.Println(">> ", err)
		return nil, err
	}

	return
}
