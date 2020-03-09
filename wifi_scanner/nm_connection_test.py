from nm_connection import *

def test_Invitados_JaverianaCali():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	"""
		Invitados_JaverianaCali function will connect to the
		best signal AP with ssid "Invitados JaverianaCali".
	"""
	print(Invitados_JaverianaCali())
	print("Finish")

def test_JaverianaCali():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	"""
		JaverianaCali function will connect to the best
		signal AP with ssid "JaverianaCali" using the user and
		password provided.
	"""
	print(JaverianaCali("laquiroz","La2208"))
	print("Finish")
	

def test_get_all_ap_info():
	"""
		get_all_ap_info function will return a list of a directories
		with all access point found by the wireless device card
	"""
	for e in get_all_ap_info():
		print(e)

def test0():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	"""
		connecttoAP will try to connect to a specific ssid (if provided)
		or to a bssid (if provided and found) using the password and user
		or the password or none as security information
	"""
	"""
	#JaverianaCali
	print(connecttoAP('',bssid="D8:54:A2:8B:DA:65",
							password="password",user="user"))
	#JaverianaCali
	print(connecttoAP('JaverianaCali',password="password",user="user"))
	
	#JaverianaCali
	print(connecttoAP('JaverianaCali',bssid="D8:54:A2:8B:DA:65",
							password="password",user="user"))
	#"Invitados JaverianaCali"
	print(connecttoAP('',bssid="9C:5D:12:8F:99:26"))
	"""
	#"Invitados JaverianaCali"
	print(connecttoAP('Invitados JaverianaCali'))
	print("Finish")

def testb0():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP("",bssid="CC:35:40:98:A8:3F",password="vmcv1234"))
	print("Finish")

def test01():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP('JaverianaCali',password="password",user="user"))
	print("Finish")

def test02():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP('Invitados JaverianaCali'))
	print("Finish")

#test_get_all_ap_info()
#test0()
#input("seguir")
test_JaverianaCali()


