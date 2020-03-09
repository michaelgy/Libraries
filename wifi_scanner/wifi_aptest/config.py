sync_time = 3600 #tiempo entre sincronización con la base de datos
sample_time = 10#10800 #seconds [3 hours]
reconnect_time = 3#600 #seconds [10 minutes]
count = 10 #cantidad de pings a realizar
interval = 0.5 #tiempo entre pings
timeout = 2 #tiempo de espera maximo de respuesta
deadline = (timeout+interval)*count+5 #tiempo de espera maximo de ejecución del comando ping
#url_servicio = "https://monitoreowifi.javerianacali.edu.co/MonitoreoWifi/logproceso/"
url_servicio = "http://127.0.0.1:8090" #test server

data_file_ext = "json"
files_path = "/home/pi/Documents/nm_dbus_python/wifi_aptest"
datetime_format_file = "%Y-%m-%d_%H-%M-%S-%f"
datetime_format_data = "%d/%m/%Y %H:%M:%S"
