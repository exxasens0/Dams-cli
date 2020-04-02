package fetching

import (
	"fmt"
	structs "github.com/exxasens0/Dams-cli/internal"
	"github.com/exxasens0/Dams-cli/internal/api"
	"github.com/exxasens0/Dams-cli/internal/displaying"
	damscli "github.com/exxasens0/Dams-cli/internal/server/http"
	"github.com/exxasens0/Dams-cli/internal/storage/csv"
	"log"
	"net/http"
	"strings"
)

type Service interface {
	FetchSensorValuesByDesc(damscli.DamsRepo, string) ([]structs.SensorData, error)
	FetchSensorDataBySensorName(damscli.DamsRepo, string) ([]structs.SensorData, error)
	FetchSensorDataByRiverName(damscli.DamsRepo, string) ([]structs.SensorData, error)
	FetchAndShowValuesBySensorName(damscli.DamsRepo, string, string, string) error
	FetchAndShowDataByRiverName(damscli.DamsRepo, string, string, string) error
	FetchAndShowValuesByDesc(damscli.DamsRepo, string, string, string) error
}

func FetchSensorValuesByDesc(repository damscli.DamsRepo, desc string) (sensordata []structs.SensorData, err error) {
	dams, _ := repository.JSONToStructDamData()
	values, _ := repository.JSONToStructSensorData()

	//iterates on sensors struct
	for _, value := range values {
		for _, sensord := range value.Sensors {
			for _, sensorv := range sensord.Observations {
				//Iterando por los sensores
				for _, dam := range dams[0].Providers[0].Sensors {
					if (dam.Sensor == sensord.Sensor) && (strings.Contains(strings.ToUpper(dam.Description), strings.ToUpper(desc)) || desc == "*" || strings.ToUpper(desc) == "ALL") {
						data := structs.SensorData{
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

func FetchSensorDataBySensorName(repository damscli.DamsRepo, sensorName string) (sensordata []structs.SensorData, err error) {
	dams, _ := repository.JSONToStructDamData()
	for _, dam := range dams {
		//Iterando por los sensores
		for _, sensord := range dam.Providers[0].Sensors {
			if strings.Contains(strings.ToUpper(sensord.Sensor), strings.ToUpper(sensorName)) || sensorName == "*" || strings.ToUpper(sensorName) == "ALL" {
				data := structs.SensorData{
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

func FetchSensorDataByRiverName(repository damscli.DamsRepo, river string) (sensordata []structs.SensorData, err error) {
	dams, _ := repository.JSONToStructDamData()
	for _, dam := range dams {
		//Iterando por los sensores
		for _, sensord := range dam.Providers[0].Sensors {
			if strings.Contains(strings.ToUpper(sensord.ComponentAdditionalInfo.Riu), strings.ToUpper(river)) || river == "*" || strings.ToUpper(river) == "ALL" {
				data := structs.SensorData{
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

func FetchSensorValuesBySensorName(repository damscli.DamsRepo, desc string) (sensordata []structs.SensorData, err error) {
	dams, _ := repository.JSONToStructDamData()
	values, _ := repository.JSONToStructSensorData()

	//iterates on sensors struct
	for _, value := range values {
		for _, sensord := range value.Sensors {
			for _, sensorv := range sensord.Observations {
				//Iterando por los sensores
				for _, dam := range dams[0].Providers[0].Sensors {
					if (dam.Sensor == sensord.Sensor) && (strings.Contains(strings.ToUpper(dam.Sensor), strings.ToUpper(desc)) || desc == "*" || strings.ToUpper(desc) == "ALL") {
						data := structs.SensorData{
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

func FetchAndShowValuesBySensorName(repository damscli.DamsRepo, filter string, flagSaveToCSV string, flagCreateEndpoint string) (err error) {
	//show sensor which contains "percentatge" string on its description
	sensordata, _ := FetchSensorValuesBySensorName(repository, filter)
	//print values in the screen
	displaying.PrintSensorValues(sensordata)
	//check if save to csv option is set
	if flagSaveToCSV != "" {
		csv.SaveSensorValuesToCSV(sensordata, flagSaveToCSV)
	}
	//Looks forward endpoint flag and if then fetch sensor by name and opens a server on defined endpoint
	if flagCreateEndpoint != "" {
		s := api.New(sensordata, flagCreateEndpoint)
		fmt.Println("The dam server is on tap now: http://localhost:8080 ande endpoint:", flagCreateEndpoint)
		log.Fatal(http.ListenAndServe(":8080", s.Router()))
	}

	return nil

}

func FetchAndShowDataByRiverName(repository damscli.DamsRepo, filter string, flagSaveToCSV string, flagCreateEndpoint string) (err error) {
	//show sensor which contains "percentatge" string on its description
	sensordata, _ := FetchSensorDataByRiverName(repository, filter)
	//print values in the screen
	displaying.PrintSensorData(sensordata)
	//check if save to csv option is set
	if flagSaveToCSV != "" {
		csv.SaveSensorValuesToCSV(sensordata, flagSaveToCSV)
	}
	//Looks forward endpoint flag and if then fetch sensor by name and opens a server on defined endpoint
	if flagCreateEndpoint != "" {
		s := api.New(sensordata, flagCreateEndpoint)
		fmt.Println("The dam server is on tap now: http://localhost:8080 ande endpoint:", flagCreateEndpoint)
		log.Fatal(http.ListenAndServe(":8080", s.Router()))
	}

	return nil

}

func FetchAndShowValuesByDesc(repository damscli.DamsRepo, filter string, flagSaveToCSV string, flagCreateEndpoint string) (err error) {
	//show sensor which contains "percentatge" string on its description
	sensordata, _ := FetchSensorValuesByDesc(repository, filter)
	//print values in the screen
	displaying.PrintSensorValues(sensordata)
	//check if save to csv option is set
	if flagSaveToCSV != "" {
		csv.SaveSensorValuesToCSV(sensordata, flagSaveToCSV)
	}
	//Looks forward endpoint flag and if then fetch sensor by name and opens a server on defined endpoint
	if flagCreateEndpoint != "" {
		s := api.New(sensordata, flagCreateEndpoint)
		fmt.Println("The dam server is on tap now: http://localhost:8080 ande endpoint:", flagCreateEndpoint)
		log.Fatal(http.ListenAndServe(":8080", s.Router()))
	}

	return nil

}

func FetchAndShowDataBySensorName(repository damscli.DamsRepo, filter string, flagSaveToCSV string, flagCreateEndpoint string) (err error) {
	//show sensor which contains "percentatge" string on its description
	sensordata, _ := FetchSensorDataBySensorName(repository, filter)
	//print values in the screen
	displaying.PrintSensorData(sensordata)
	//check if save to csv option is set
	if flagSaveToCSV != "" {
		csv.SaveSensorValuesToCSV(sensordata, flagSaveToCSV)
	}
	//Looks forward endpoint flag and if then fetch sensor by name and opens a server on defined endpoint
	if flagCreateEndpoint != "" {
		s := api.New(sensordata, flagCreateEndpoint)
		fmt.Println("The dam server is on tap now: http://localhost:8080 ande endpoint:", flagCreateEndpoint)
		log.Fatal(http.ListenAndServe(":8080", s.Router()))
	}

	return nil

}
