package csv

import (
	damscli "github.com/exxasens0/Dams-cli/internal"
)

const (
	csvFile = "github.com/exxasens0/Dams-cli/data/package.json"
)

// DamsRepo definiton of methods to access a data
type DamsRepo interface {
	JSONToStructDamData() ([]damscli.Dam, error)
	JSONToStructSensorData() ([]damscli.SensorValue, error)
}

type damsRepo struct {
	url string
}

func NewCSVRepository() DamsRepo {
	return &damsRepo{}
}

//TODO
//Get all dam Data
func (b *damsRepo) JSONToStructDamData() (dams []damscli.Dam, err error) {

	return
}

//TODO
//Get values from a sensor defined
func (b *damsRepo) JSONToStructSensorData() (sensorvalues []damscli.SensorValue, err error) {

	return
}
