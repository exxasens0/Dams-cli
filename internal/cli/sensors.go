package cli

import (
	"fmt"
	fetching "github.com/exxasens0/Dams-cli/internal/fetching"
	damscli "github.com/exxasens0/Dams-cli/internal/server/http"
	"github.com/spf13/cobra"
)

func InitSensoresCmd(repository damscli.DamsRepo) *cobra.Command {
	var sensorsCmd = &cobra.Command{
		Use:   "sensor",
		Short: "Imprime los sensores configurados por rio",
		Run:   runSensorsFn(repository),
	}
	//flags defined
	sensorsCmd.Flags().StringP("sensor", "r", "", "Muestra información asociada a un sensor")
	sensorsCmd.Flags().BoolP("all", "a", false, "Muestra la información asociada de todos los sensores configurados")
	sensorsCmd.Flags().StringP("save", "s", "", "guarda en archivo csv la información de los sensores configurados ")
	sensorsCmd.Flags().StringP("endpoint", "e", "", "inicia server para peticiones post con el endpoint definido ")

	return sensorsCmd
}

func runSensorsFn(repository damscli.DamsRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
		endpoint, _ := cmd.Flags().GetString("endpoint")

		//Fetch sensor by name and show and writes to csv file
		flagS, _ := cmd.Flags().GetString("sensor")
		if flagS != "" {
			fetching.FetchAndShowDataBySensorName(repository, flagS, savetoCSV, endpoint)
			return
		}

		//fetch all sensors and show and writes to csv file
		flag, _ := cmd.Flags().GetBool("all")
		if flag {
			fetching.FetchAndShowDataBySensorName(repository, "all", savetoCSV, endpoint)
			return
		}

		fmt.Println("opcion disponible unicamente con flags -r o -a ")

	}
}
