package cli

import (
	"fmt"
	fetching "github.com/exxasens0/Dams-cli/internal/fetching"
	damcli "github.com/exxasens0/Dams-cli/internal/server/http"
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
	riosCmd.Flags().StringP("endpoint", "e", "", "inicia server para peticiones post con el endpoint definido ")

	return riosCmd
}

func runRiosFn(repository damcli.DamsRepo) func(cmd *cobra.Command, args []string) {
	return func(cmd *cobra.Command, args []string) {

		savetoCSV, _ := cmd.Flags().GetString("save") //savetoCSV contains csv name
		endpoint, _ := cmd.Flags().GetString("endpoint")

		//Fetch sensor by name and show and writes to csv file
		flagS, _ := cmd.Flags().GetString("rios")
		if flagS != "" {
			fetching.FetchAndShowDataByRiverName(repository, flagS, savetoCSV, endpoint)
			return
		}

		//fetch all sensors and show and writes to csv file
		flag, _ := cmd.Flags().GetBool("all")
		if flag {
			fetching.FetchAndShowDataByRiverName(repository, "all", savetoCSV, endpoint)
			return
		}

		fmt.Println("opcion disponible unicamente con flags -r o -a ")

	}

}
