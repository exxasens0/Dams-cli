package structs

// Beer representation of beer into data struct
type Dam struct {
	Providers []struct {
		Permission string `json:"permission"`
		Provider   string `json:"provider"`
		Sensors    []struct {
			AdditionalInfo struct {
				Rang_maxim          string `json:"Rang màxim"`
				Rang_minim          string `json:"Rang mínim"`
				Temps_mostreig__min string `json:"Temps mostreig (min)"`
			} `json:"additionalInfo"`
			Component               string `json:"component"`
			ComponentAdditionalInfo struct {
				Capacitat_maxima_embassament string `json:"Capacitat màxima embassament"`
				Comarca                      string `json:"Comarca"`
				Conca                        string `json:"Conca"`
				Districte_fluvial            string `json:"Districte fluvial"`
				Provincia                    string `json:"Província"`
				Riu                          string `json:"Riu"`
				Subconca                     string `json:"Subconca"`
				Terme_municipal              string `json:"Terme municipal"`
			} `json:"componentAdditionalInfo"`
			ComponentDesc             string `json:"componentDesc"`
			ComponentPublicAccess     bool   `json:"componentPublicAccess"`
			ComponentTechnicalDetails struct {
				Connectivity string `json:"connectivity"`
				Energy       string `json:"energy"`
				MacAddress   string `json:"macAddress"`
				Model        string `json:"model"`
				Producer     string `json:"producer"`
				SerialNumber string `json:"serialNumber"`
			} `json:"componentTechnicalDetails"`
			ComponentType    string `json:"componentType"`
			DataType         string `json:"dataType"`
			Description      string `json:"description"`
			Location         string `json:"location"`
			PublicAccess     bool   `json:"publicAccess"`
			Sensor           string `json:"sensor"`
			TechnicalDetails struct {
				Energy       string `json:"energy"`
				Model        string `json:"model"`
				Producer     string `json:"producer"`
				SerialNumber string `json:"serialNumber"`
			} `json:"technicalDetails"`
			TimeZone string `json:"timeZone"`
			Type     string `json:"type"`
			Unit     string `json:"unit"`
		} `json:"sensors"`
	} `json:"providers"`
}

type SensorValue struct {
	Sensors []struct {
		Sensor       string `json:"sensor"`
		Observations []struct {
			Value     string `json:"value"`
			Timestamp string `json:"timestamp"`
			Location  string `json:"location"`
		} `json:"observations"`
	} `json:"sensors"`
}

type SensorData struct {
	Dam         string `json:"dam"`
	River       string `json:"river"`
	SensorName  string `json:"sensorname"`
	Description string `json:"description"`
	Value       string `json:"value"`
	Timestamp   string `json:"timestamp"`
}
