package http

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	damscli "github.com/exxasens0/Dams-cli/internal"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	_ "strings"
)

const (
	sensorValueEndPoint = "/sdim2/apirest/data/EMBASSAMENT-EST"
	productsEndpoint    = "/sdim2/apirest/catalog?componentType=embassament"
	damsURL             = "http://aca-web.gencat.cat"
)

type damsRepo struct {
	url string
}

func NewWWWRepository() damscli.DamsRepo {
	return &damsRepo{url: damsURL}
}

func (b *damsRepo) FetchSensorDataBySensorName(sensorName string) (sensordata []damscli.SensorData, err error) {
	dams, _ := b.apiJSONToStructDamData()
	for _, dam := range dams {
		//Iterando por los sensores
		for _, sensord := range dam.Providers[0].Sensors {
			if strings.Contains(strings.ToUpper(sensord.Sensor), strings.ToUpper(sensorName)) || sensorName == "*" || strings.ToUpper(sensorName) == "ALL" {
				data := damscli.SensorData{
					Dam:         sensord.ComponentDesc,
					River:       sensord.ComponentAdditionalInfo.Riu,
					SensorName:  sensord.Sensor,
					Description: sensord.Description,
				}
				sensordata = append(sensordata, data)
			}
		}
	}
	return
}

func (b *damsRepo) FetchSensorDataByRiverName(river string) (sensordata []damscli.SensorData, err error) {
	dams, _ := b.apiJSONToStructDamData()
	for _, dam := range dams {
		//Iterando por los sensores
		for _, sensord := range dam.Providers[0].Sensors {
			if strings.Contains(strings.ToUpper(sensord.ComponentAdditionalInfo.Riu), strings.ToUpper(river)) || river == "*" || strings.ToUpper(river) == "ALL" {
				data := damscli.SensorData{
					Dam:         sensord.ComponentDesc,
					River:       sensord.ComponentAdditionalInfo.Riu,
					SensorName:  sensord.Sensor,
					Description: sensord.Description,
				}
				sensordata = append(sensordata, data)
			}
		}
	}
	return
}

func (b *damsRepo) FetchSensorValuesBySensorName(desc string) (sensordata []damscli.SensorData, err error) {
	dams, _ := b.apiJSONToStructDamData()
	values, _ := b.apiJSONToStructSensorData()

	//iterates on sensors struct
	for _, value := range values {
		for _, sensord := range value.Sensors {
			for _, sensorv := range sensord.Observations {
				//Iterando por los sensores
				for _, dam := range dams[0].Providers[0].Sensors {
					if (dam.Sensor == sensord.Sensor) && (strings.Contains(strings.ToUpper(dam.Sensor), strings.ToUpper(desc)) || desc == "*" || strings.ToUpper(desc) == "ALL") {
						data := damscli.SensorData{
							Dam:         dam.ComponentDesc,
							River:       dam.ComponentAdditionalInfo.Riu,
							SensorName:  sensord.Sensor,
							Value:       sensorv.Value,
							Description: dam.Description,
							Timestamp:   sensorv.Timestamp,
						}
						sensordata = append(sensordata, data)
						break
					}
				}
			}
		}
	}

	return
}

func (b *damsRepo) FetchSensorValuesByDesc(desc string) (sensordata []damscli.SensorData, err error) {
	dams, _ := b.apiJSONToStructDamData()
	values, _ := b.apiJSONToStructSensorData()

	//iterates on sensors struct
	for _, value := range values {
		for _, sensord := range value.Sensors {
			for _, sensorv := range sensord.Observations {
				//Iterando por los sensores
				for _, dam := range dams[0].Providers[0].Sensors {
					if (dam.Sensor == sensord.Sensor) && (strings.Contains(strings.ToUpper(dam.Description), strings.ToUpper(desc)) || desc == "*" || strings.ToUpper(desc) == "ALL") {
						data := damscli.SensorData{
							Dam:         dam.ComponentDesc,
							River:       dam.ComponentAdditionalInfo.Riu,
							SensorName:  sensord.Sensor,
							Value:       sensorv.Value,
							Description: dam.Description,
							Timestamp:   sensorv.Timestamp,
						}
						sensordata = append(sensordata, data)
						break
					}
				}
			}
		}
	}

	return
}

func (b *damsRepo) PrintSensorData(sensordata []damscli.SensorData) (err error) {
	for _, sensor := range sensordata {
		fmt.Println("Sensor Name:", sensor.SensorName,
			"| Dam:", sensor.Dam,
			"| River:", sensor.River,
			"| Description:", sensor.Description,
		)
	}

	return
}

func (b *damsRepo) PrintSensorValues(sensordata []damscli.SensorData) (err error) {
	for _, sensor := range sensordata {
		fmt.Println("Timestamp:", sensor.Timestamp,
			"| Value:", sensor.Value,
			"| Sensor Name:", sensor.SensorName,
			"| Dam:", sensor.Dam, "River:", sensor.River,
			"| Description:", sensor.Description,
		)
	}

	return
}

func (b *damsRepo) SaveSensorValuesToCSV(sensordata []damscli.SensorData, filename string) (err error) {
	//check filename extension
	if !strings.Contains(".csv", filename) {
		filename = filename + ".csv"
	}
	//creates file
	file, _ := os.Create(filename)
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, sensor := range sensordata {
		var record []string
		//writer expects and [] string array
		record = append(record, sensor.Timestamp)
		record = append(record, sensor.Value)
		record = append(record, sensor.Dam)
		record = append(record, sensor.River)
		record = append(record, sensor.SensorName)
		record = append(record, sensor.Description)
		writer.Write(record)
	}

	return
}

func (b *damsRepo) SaveSensorDataToCSV(sensordata []damscli.SensorData, filename string) (err error) {
	//check filename extension
	if !strings.Contains(".csv", filename) {
		filename = filename + ".csv"
	}
	//creates file
	file, _ := os.Create(filename)
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, sensor := range sensordata {
		var record []string
		//writer expects and [] string array
		record = append(record, sensor.SensorName)
		record = append(record, sensor.Dam)
		record = append(record, sensor.River)
		record = append(record, sensor.Description)
		writer.Write(record)
	}

	return
}

//Get all dam Data
func (b *damsRepo) apiJSONToStructDamData() (dams []damscli.Dam, err error) {
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

//Get values from a sensor defined
func (b *damsRepo) apiJSONToStructSensorData() (sensorvalues []damscli.SensorValue, err error) {
	response, err := http.Get(fmt.Sprintf("%v%v", b.url, sensorValueEndPoint))

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

func insertByte(array []byte, index int, value byte) []byte {
	return append(array[:index], append([]byte{value}, array[index:]...)...)
}
