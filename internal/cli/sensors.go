package cli

import (
	"fmt"
	"log"
	"net/http"

	damcli "github.com/exxasens0/Dams-cli/internal"
	"github.com/exxasens0/gDams-cli/internal/api"
	"github.com/spf13/cobra"
)

func InitSensoresCmd(repository damcli.DamsRepo) *cobra.Command {
	var sensorsCmd = &cobra.Command{
		Use:   "sensor",
		Short: "Imprime los sensores configurados por rio",
		Run:   runSensorsFn(repository),
	}
	//flags defined
	sensorsCmd.Flags().StringP("sensor", "r", "", "Muestra información asociada a un sensor")
	sensorsCmd.Flags().BoolP("all", "a", false, "Muestra la información asociada de todos los sensores configurados")
	sensorsCmd.Flags().StringP("save", "s", "", "guarda en archivo csv la información de los sensores configurados ")
	sensorsCmd.Flags().StringP("endpoint", "v", "", "inicia server para peticiones post con el endpoint definido ")

	return sensorsCmd
}

func runSensorsFn(repository damcli.DamsRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		var sensordata []damcli.SensorData
		var
		//Fetch sensor by name and show and writes to csv file
		sensor, _ = cmd.Flags().GetString("sensor")

		if sensor != "" {
			sensordata, _ = repository.FetchSensorDataBySensorName(sensor)
			//print values in the screen
			repository.PrintSensorData(sensordata)
		}

		//fetch all sensors and show and writes to csv file
		all, _ := cmd.Flags().GetBool("all")

		if all {
			sensordata, _ = repository.FetchSensorDataBySensorName("*")
			//print values in the screen
			repository.PrintSensorData(sensordata)
		}

		//check if save to csv option is set
		savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
		if savetoCSV != "" {
			repository.SaveSensorDataToCSV(sensordata, savetoCSV)
		}
		//Fetch sensor by name and opens a server
		endpoint, _ := cmd.Flags().GetString("endpoint")
		if endpoint != "" {
			s := api.New(sensordata, endpoint)
			fmt.Println("The dam server is on tap now: http://localhost:8080 ande endpoint:", endpoint)
			log.Fatal(http.ListenAndServe(":8080", s.Router()))
		}

		fmt.Println("opcion no reconocida")
	}
}
