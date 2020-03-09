#!/bin/bash
curl -i -X POST http://replica.javerianacali.edu.co:8090/MonitoreoWifi/evaluacionRed -d '{"ssidMac":"99:00:11:22", "macRaspberry":"12:34:56:67", "dbm":1243, "tpMax":45678, "tpMin":4556, "tpAvg":877, "tpLoss":333, "codigoRed":1,"codBandaFrecuencia":1, "codPruebaBandaFrec":1, "conecta":1}'
#./sql MONITOREOWIFI/roundrabbit40@svrorarep.puj.edu.co:1521/HR9PRDB

#import jaydebeapi
#cprop = {'user':'MONITOREOWIFI','password':'roundrabbit40'}
#conn = jaydebeapi.connect("org.hsqldb.jdbcDriver","svrorarep.puj.edu.co:1521/HR9PRDB",cprop)