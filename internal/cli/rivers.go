package cli

import (
	damcli "github.com/exxasens0/Dams-cli/internal"
	"github.com/spf13/cobra"
)

func InitRiosCmd(repository damcli.DamsRepo) *cobra.Command {
	var riosCmd = &cobra.Command{
		Use:   "rio",
		Short: "Imprime los diferentes rios y los sensores asociados",
		Run:   runRiosFn(repository),
	}
	//flags defined
	riosCmd.Flags().StringP("rios", "r", "", "Sensores asociados para un rio concreto, ")
	riosCmd.Flags().BoolP("all", "a", false, "Muestra la información asociada de todos los rios presentes")
	riosCmd.Flags().StringP("save", "s", "", "guarda en archivo csv la información de los rios ")

	return riosCmd
}

func runRiosFn(repository damcli.DamsRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		//Fetch sensor by name and show and writes to csv file
		rio, _ := cmd.Flags().GetString("rios")

		if rio != "" {
			sensordata, _ := repository.FetchSensorDataByRiverName(rio)
			//print values in the screen
			repository.PrintSensorData(sensordata)
			//check if save to csv option is set
			savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
			if savetoCSV != "" {
				repository.SaveSensorDataToCSV(sensordata, savetoCSV)
			}

			return
		}

		//fetch all sensors and show and writes to csv file
		all, _ := cmd.Flags().GetBool("all")

		if all {
			sensordata, _ := repository.FetchSensorDataByRiverName("*")
			//print values in the screen
			repository.PrintSensorData(sensordata)
			//check if save to csv option is set
			savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
			if savetoCSV != "" {
				repository.SaveSensorDataToCSV(sensordata, savetoCSV)
			}
			return
		}

	}
}
