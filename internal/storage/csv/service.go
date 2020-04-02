package csv

import (
	"encoding/csv"
	structs "github.com/exxasens0/Dams-cli/internal"
	"os"
	"strings"
)

type Service interface {
	SaveSensorValuesToCSV([]structs.SensorData, string) error
	SaveSensorDataToCSV([]structs.SensorData, string) error
}

func SaveSensorValuesToCSV(sensordata []structs.SensorData, filename string) (err error) {
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

func SaveSensorDataToCSV(sensordata []structs.SensorData, filename string) (err error) {
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
