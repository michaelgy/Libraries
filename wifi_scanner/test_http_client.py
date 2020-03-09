import requests
test_json = {
    "ssidMac":"99:00:11:22",
    "macRaspberry":"12:34:56:67",
    "dbm":1243,
    "tpMax":45678,
    "tpMin":4556,
    "tpAvg":877,
    "tpLoss":333,
    "codigoRed":1,
    "codBandaFrecuencia":1,
    "codPruebaBandaFrec":1,
    "conecta":1
}
url = "http://replica.javerianacali.edu.co:8090/MonitoreoWifi/evaluacionRed/"
r = requests.post(url, json=test_json)
print(r.status_code)
print(r.content)