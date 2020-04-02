package main

import (
	"flag"
	"github.com/exxasens0/Dams-cli/internal"
	"github.com/exxasens0/Dams-cli/internal/cli"
	"github.com/exxasens0/Dams-cli/internal/server/csv"
	"github.com/exxasens0/Dams-cli/internal/server/http"
	"github.com/spf13/cobra"
)

func main() {

	csvData := flag.Bool("csv", false, "load data from csv")
	flag.Parse()

	var repo DamsRepo

	if *csvData {
		repo = csv.NewCSVRepository()
	} else {
		repo = http.NewWWWRepository()
	}

	rootCmd := &cobra.Command{Use: "dam-cli"}
	rootCmd.AddCommand(cli.InitSensoresCmd(repo))
	rootCmd.AddCommand(cli.InitRiosCmd(repo))
	rootCmd.AddCommand(cli.InitValuesCmd(repo))
	rootCmd.Execute()

}
