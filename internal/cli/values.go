package cli

import (
	"fmt"
	fetching "github.com/exxasens0/Dams-cli/internal/fetching"
	damscli "github.com/exxasens0/Dams-cli/internal/server/http"
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
	valuesCmd.Flags().StringP("endpoint", "e", "", "inicia server para peticiones post con el endpoint definido")

	return valuesCmd
}

func runValuesFn(repository damscli.DamsRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
		endpoint, _ := cmd.Flags().GetString("endpoint")

		//show all sensor data
		flagS, _ := cmd.Flags().GetString("sensor")
		if flagS != "" {
			fetching.FetchAndShowValuesBySensorName(repository, flagS, savetoCSV, endpoint)
			return
		}
		//show all  data
		flag, _ := cmd.Flags().GetBool("all")

		if flag {
			fetching.FetchAndShowValuesBySensorName(repository, "all", savetoCSV, endpoint)
			return
		}

		//show all volume data
		flag, _ = cmd.Flags().GetBool("volum")

		if flag {
			fetching.FetchAndShowValuesByDesc(repository, "volum", savetoCSV, endpoint)
			return
		}

		//show all level data
		flag, _ = cmd.Flags().GetBool("nivel")

		if flag {
			fetching.FetchAndShowValuesByDesc(repository, "nivel", savetoCSV, endpoint)
			return
		}

		fmt.Println("opcion no reconocida")
	}
}
