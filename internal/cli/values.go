package cli

import (
	"fmt"
	damscli "github.com/exxasens0/Dams-cli/internal"
	"github.com/spf13/cobra"
)

func InitValuesCmd(repository damscli.DamsRepo) *cobra.Command {
	var valuesCmd = &cobra.Command{
		Use:   "values",
		Short: "Imprime los valores por embalse de volumen o nivel",
		Run:   runValuesFn(repository),
	}
	//flags defined
	valuesCmd.Flags().BoolP("volum", "v", false, "valor de volumen")
	valuesCmd.Flags().BoolP("nivel", "n", false, "valor de nivel")
	valuesCmd.Flags().BoolP("all", "a", false, "todos los valores")
	valuesCmd.Flags().StringP("sensor", "r", "", "Muestra los datos asociados a un sensor")
	valuesCmd.Flags().StringP("save", "s", "", "guarda en archivo csv la información de los sensores filtrados ")
	valuesCmd.Flags().StringP("post", "p", "values", "post values through server localhost:8080/ <endpoint>")

	return valuesCmd
}

func runValuesFn(repository damscli.DamsRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		//show all sensor data
		flagS, _ := cmd.Flags().GetString("sensor")

		if flagS != "" {
			//show sensor values
			sensordata, _ := repository.FetchSensorValuesBySensorName(flagS)
			//print values in the screen
			repository.PrintSensorValues(sensordata)
			//check if save to csv option is set
			savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
			if savetoCSV != "" {
				repository.SaveSensorValuesToCSV(sensordata, savetoCSV)
			}

			return
		}

		//show all volume data
		flag, _ := cmd.Flags().GetBool("volum")

		if flag {
			//show sensor which contains "percentatge" string on its description
			sensordata, _ := repository.FetchSensorValuesByDesc("percentatge")
			//print values in the screen
			repository.PrintSensorValues(sensordata)
			//check if save to csv option is set
			savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
			if savetoCSV != "" {
				repository.SaveSensorValuesToCSV(sensordata, savetoCSV)
			}

			return
		}

		//show all level data
		flag, _ = cmd.Flags().GetBool("nivel")

		if flag {
			//show sensor which contains "percentatge" string on its description
			sensordata, _ := repository.FetchSensorValuesByDesc("nivel")
			//print values in the screen
			repository.PrintSensorValues(sensordata)
			//check if save to csv option is set
			savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
			if savetoCSV != "" {
				repository.SaveSensorValuesToCSV(sensordata, savetoCSV)
			}
			return
		}

		//show all  data
		flag, _ = cmd.Flags().GetBool("all")

		if flag {
			//show sensor which contains "percentatge" string on its description
			sensordata, _ := repository.FetchSensorValuesBySensorName("*")
			//print values in the screen
			repository.PrintSensorValues(sensordata)
			//check if save to csv option is set
			savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
			if savetoCSV != "" {
				repository.SaveSensorValuesToCSV(sensordata, savetoCSV)
			}
			return
		}

		endpoint, _ := cmd.Flags().GetString("post")

		if endpoint != "" {
			//show sensor which contains "nivel" string on its description
			//handleFuncValues(dams, values, endpoint,  endpoint )
			return
		}

		fmt.Println("opcion no reconocida")
	}
}
