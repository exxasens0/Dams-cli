package displaying

import (
	"fmt"
	structs "github.com/exxasens0/Dams-cli/internal"
)

type Service interface {
	PrintSensorValues([]structs.SensorData) error
	PrintSensorData([]structs.SensorData) error
}

func PrintSensorData(sensordata []structs.SensorData) (err error) {
	for _, sensor := range sensordata {
		fmt.Println("Sensor Name:", sensor.SensorName,
			"| Dam:", sensor.Dam,
			"| River:", sensor.River,
			"| Description:", sensor.Description,
		)
	}

	return
}

func PrintSensorValues(sensordata []structs.SensorData) (err error) {
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
