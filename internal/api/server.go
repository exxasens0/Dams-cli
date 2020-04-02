package api

import (
	"encoding/json"
	damscli "github.com/exxasens0/Dams-cli/internal"
	"github.com/gorilla/mux"
	"net/http"
)

type api struct {
	router     http.Handler
	sensordata []damscli.SensorData
}

type Server interface {
	Router() http.Handler
}

func New(sensordata []damscli.SensorData, endpoint string) Server {
	a := &api{}
	a.sensordata = sensordata

	r := mux.NewRouter()
	r.HandleFunc("/"+endpoint, a.updateEvent).Methods(http.MethodGet)

	a.router = r
	return a
}

func (a *api) Router() http.Handler {
	return a.router
}

func (a *api) updateEvent(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(a.sensordata)
}
