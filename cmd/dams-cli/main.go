package main

import (
	"flag"
	"github.com/exxasens0/Dams-cli/internal/cli"
	"github.com/exxasens0/Dams-cli/internal/server/csv"
	"github.com/exxasens0/Dams-cli/internal/server/http"
	"github.com/spf13/cobra"
)

func main() {

	csvData := flag.Bool("csv", false, "load data from csv")
	flag.Parse()

	var repoDam http.DamsRepo
	var repoSensor http.SensorRepo

	if *csvData {
		repoDam = csv.NewCSVRepository()
	} else {
		repoDam = http.NewDamRepositoryFromHttp()
		repoSensor = http.NewSensorepositoryFromHttp()
	}

	rootCmd := &cobra.Command{Use: "dam-cli"}
	rootCmd.AddCommand(cli.InitSensoresCmd(repoDam))
	rootCmd.AddCommand(cli.InitRiosCmd(repoDam))
	rootCmd.AddCommand(cli.InitValuesCmd(repoDam, repoSensor)) //Dam data + Sensor Data
	rootCmd.Execute()

}
