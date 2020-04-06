package cli

import (
	"fmt"
	fetching "github.com/exxasens0/Dams-cli/internal/fetching"
	damscli "github.com/exxasens0/Dams-cli/internal/server/http"
	"github.com/spf13/cobra"
)

func InitValuesCmd(repoDam damscli.DamsRepo, repoSensor damscli.SensorRepo) *cobra.Command {
	var valuesCmd = &cobra.Command{
		Use:   "values",
		Short: "Imprime los valores por embalse de volumen o nivel",
		Run:   runValuesFn(repoDam, repoSensor),
	}
	//flags defined
	valuesCmd.Flags().BoolP("volum", "v", false, "valor de volumen")
	valuesCmd.Flags().BoolP("nivel", "n", false, "valor de nivel")
	valuesCmd.Flags().BoolP("all", "a", false, "todos los valores")
	valuesCmd.Flags().StringP("sensor", "r", "", "Muestra los datos asociados a un sensor")
	valuesCmd.Flags().StringP("save", "s", "", "guarda en archivo csv la información de los sensores filtrados ")
	valuesCmd.Flags().StringP("endpoint", "e", "", "inicia server para peticiones post con el endpoint definido")

	return valuesCmd
}

func runValuesFn(repoDam damscli.DamsRepo, repoSensor damscli.SensorRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
		endpoint, _ := cmd.Flags().GetString("endpoint")

		//show all sensor data
		flagS, _ := cmd.Flags().GetString("sensor")
		if flagS != "" {
			fetching.FetchAndShowValuesBySensorName(repoDam, repoSensor, flagS, savetoCSV, endpoint)
			return
		}
		//show all  data
		flag, _ := cmd.Flags().GetBool("all")

		if flag {
			fetching.FetchAndShowValuesBySensorName(repoDam, repoSensor, "all", savetoCSV, endpoint)
			return
		}

		//show all volume data
		flag, _ = cmd.Flags().GetBool("volum")

		if flag {
			fetching.FetchAndShowValuesByDesc(repoDam, repoSensor, "volum", savetoCSV, endpoint)
			return
		}

		//show all level data
		flag, _ = cmd.Flags().GetBool("nivel")

		if flag {
			fetching.FetchAndShowValuesByDesc(repoDam, repoSensor, "nivel", savetoCSV, endpoint)
			return
		}

		fmt.Println("opcion no reconocida")
	}
}
