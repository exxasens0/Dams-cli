#Ejemplo CLI con GO
##cli-dam: estado de los embalses en Cataluña
Este ejemplo implementa funcionalidad de linea de comandos para consulta del estado del nivel y volumen de los embalses en el territorio catalán.

Permite consultar todos los sensores instalados en cada uno de los embalses, asociando información del rio, del tipo de sensor y horarios  de la toma de medidas.

#How to Run

> $ go run /cmd/dams-cli/main.go 


#Funciones
##Sensores
Muestra la información asociada a los sensores definidos dentro de los distintos rios y embalses.
La información facilitada por sensor será el embalse al que pertenece así como el río y la descripción del tipo de sensor (volumen, nivel en %, nivel absoluto)
> $ go run /cmd/dams-cli/main.go sensores -h
     
      Usage:
        dam-cli sensor [flags]
  
      Flags:
        -a, --all               Muestra la información asociada de todos los sensores configurados
        -e, --endpoint string   inicia server para peticiones post con el endpoint definido 
        -h, --help              help for sensor
        -s, --save string       guarda en archivo csv la información de los sensores configurados 
        -r, --sensor string     Muestra información asociada a un sensor
        
Por ejemplo:
> $ dam-cli sensor -r 1707 -s sensor1707.csv -e sensor1707

Muestra el resultado en terminal:
> Timestamp:  | Value:  | Sensor Name: CALC001707 | Dam: Susqueda (Osor) River: RIU TER | Description: Volum embassat

Guarda en el archivo sensor1707.csv la información asociada y abré un endpoint contra la dirección localhost:8080/sensor1707


##Rios
Muestra la información de sensores asociadas por rio

> $ go run /cmd/dams-cli/main.go rio -h


        Usage:
          dam-cli rio [flags]
        
        Flags:
          -a, --all               Muestra la información asociada de todos los rios presentes
          -e, --endpoint string   inicia server para peticiones post con el endpoint definido 
          -h, --help              help for rio
          -r, --rios string       Sensores asociados para un rio concreto, 
          -s, --save string       guarda en archivo csv la información de los rios

Por ejemplo:
> $ dam-cli rio -a -s rios.csv -e rios

Muestra el resultado
> Sensor Name: 080581-002-ANA006 | Dam: Foix (Castellet i la Gornal) River: RIU FOIX | Description: Nivell absolut

> Sensor Name: 081419-003-ANA005 | Dam: Llosa del Cavall (Navès) River: RIU CARDENER | Description: Nivell absolut

> Sensor Name: 082687-001-ANA015 | Dam: Baells (Cercs) River: RIU LLOBREGAT | Description: Nivell absolut

> Sensor Name: 083036-001-ANA023 | Dam: Sau (Vilanova de Sau) River: RIU TER | Description: Nivell absolut

> Sensor Name: CALC000126 | Dam: Pasteral (la Cellera de Ter) River: RIU TER | Description: Volum embassat

> Sensor Name: CALC000143 | Dam: Pasteral (la Cellera de Ter) River: RIU TER | Description: Percentatge volum embassat

> Sensor Name: CALC000145 | Dam: Sau (Vilanova de Sau) River: RIU TER | Description: Volum embassat

Guarda en el archivo rios.csv la información asociada y abré un endpoint contra la dirección localhost:8080/rios


Otro ejemplo:
> $ dam-cli rio -r ll -s rios.csv -e rios

Muestra el resultado filtrado por nombres de riu que contengan el string "ll", en este caso, llobregat

> Sensor Name: 082687-001-ANA015 | Dam: Baells (Cercs) River: RIU LLOBREGAT | Description: Nivell absolut

> Sensor Name: CALC000713 | Dam: Baells (Cercs) River: RIU LLOBREGAT | Description: Percentatge volum embassat

> Sensor Name: CALC000697 | Dam: Baells (Cercs) River: RIU LLOBREGAT | Description: Volum embassat



##Valores
Muestra los valores asociados a un sensor o a todos los sensores. Los sensores se pueden mostrar filtrados por volumen en % o bien por nivel.

> $ go run /cmd/dams-cli/main.go values -h

    Usage:
      dam-cli values [flags]
    
    Flags:
      -a, --all               todos los valores
      -e, --endpoint string   inicia server para peticiones post con el endpoint definido
      -h, --help              help for values
      -n, --nivel             valor de nivel
      -s, --save string       guarda en archivo csv la información de los sensores filtrados 
      -r, --sensor string     Muestra los datos asociados a un sensor
      -v, --volum             valor de volumen

Por ejemplo:
> $ dam-cli values -r 07 -s valoresSensor07.csv -e valoresSensor07

Muestra el valor de todos los sensores que contienen un 07 en su descripción, indicando la fecha/hora de la última medida así como el valor y datos asociados.
>Timestamp: 02/04/2020T23:25:00 | Value: 91.025 | Sensor Name: CALC000735 | Dam: Sant Ponç (Clariana de Cardener) River: RIU CARDENER | Description: Percentatge volum embassat

>Timestamp: 02/04/2020T23:25:00 | Value: 528.44 | Sensor Name: 250753-004-ANA010 | Dam: Sant Ponç (Clariana de Cardener) River: RIU CARDENER | Description: Nivell absolut

>Timestamp: 02/04/2020T23:30:00 | Value: 188.091 | Sensor Name: 171899-003-ANA007 | Dam: Pasteral (la Cellera de Ter) River: RIU TER | Description: Nivell absolut

>Timestamp: 02/04/2020T23:25:00 | Value: 95.793 | Sensor Name: CALC000713 | Dam: Baells (Cercs) River: RIU LLOBREGAT | Description: Percentatge volum embassat

>Timestamp: 02/04/2020T23:25:00 | Value: 100.043 | Sensor Name: CALC000722 | Dam: Llosa del Cavall (Navès) River: RIU CARDENER | Description: Percentatge volum embassat

>Timestamp: 02/04/2020T23:15:00 | Value: 224.333 | Sensor Name: CALC001707 | Dam: Susqueda (Osor) River: RIU TER | Description: Volum embassat


