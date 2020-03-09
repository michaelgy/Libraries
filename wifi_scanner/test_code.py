import nm_connection
#print(nm_connection.get_all_ap_info())

#fails with hidden connections
print(nm_connection.Invitados_JaverianaCali())
#print(nm_connection.connecttoAP("PUJ-TEST-INVITADO"))
#print(nm_connection.connecttoAP("HOME-A83F",password="vmcv1234"))
#print(nm_connection.connecttoAP("PUJ-TEST-CP",user="michaelguerrero",password="1405Unimath"))
#print(nm_connection.JaverianaCali("michaelguerrero","1405Unimath",timeout=20))
#nm_connection.deactive_wireless_conn()

"""
import cx_Oracle

# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
connection = cx_Oracle.connect("MONITOREOWIFI", "roundrabbit40", "svrorarep.puj.edu.co")

cursor = connection.cursor()
"""