import NetworkManager
import uuid
import time

nm = NetworkManager.NetworkManager

def accessPoints(prop,value):
	"""Function used to get available access points.
	
	:param prop: is the property that must have an access point of interest
	:type prop: str
	:param value: is the respective value that property must have
	:type value: str

	:returns: A tuple with availables access points and the wireless device
	:rtype: tuple
	"""
	devices = nm.GetAllDevices()
	wdev = None
	for dev in devices:
		#print(dev.DeviceType, dev.State, dev.Interface, dir(dev))
		if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and (dev.State == NetworkManager.NM_STATE_DISCONNECTED or dev.State == NetworkManager.NM_STATE_DISCONNECTING) and dev.Interface == 'wlo1':
			wdev = dev
			break
	acpoints = []
	#print(wdev.DeviceType, wdev.State, wdev.Interface, dir(wdev))
	for acp in wdev.GetAllAccessPoints():
		acp_attr = dir(acp)

		if prop in acp_attr and getattr(acp,prop) == value:
			acpoints.append(acp)
	return (acpoints,wdev)

def connectProfile(setting, key, value):
	"""Function used to get previously saved connection profiles.

	:param setting: is the setting that must have a connection profile
	:type setting: str
	:param key: is the respective key that a property of setting must have
	:type key: str
	:param value: is the respective value of key must have
	:type value: str

	:returns: A settings object
	"""
	connections = NetworkManager.Settings.ListConnections()
	for conn in connections:
		conn_s = conn.GetSettings()
		if setting in conn_s and key in conn_s[setting] and value == conn_s[setting][key]:
			return conn

def deactive_wireless_conn():
	"""Function used to disconnect all active wireless connections.
	"""
	for aconn in nm.ActiveConnections:
		if aconn.Type == '802-11-wireless':
			nm.DeactivateConnection(aconn)

#HwAddress is the MAC address or BSSID of the AP
#Strength is the strength of the AP signal in percent
#Frequency is the frequency band of the AP in MHz
attr_interest = ['Ssid','HwAddress','Strength','Frequency']
channel = dict([(2407+5*i,i) for i in range(1,15)])
def get_all_ap_info():
	"""Function used to get the attributes of interest of the available networks.

	:returns: a list of dictionaries with the attributes in attr_interest list
	:rtype: list
	"""
	deactive_wireless_conn()
	devices = nm.GetAllDevices()
	wdev = None
	for dev in devices:
		if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
			wdev = dev
			break
	ap_info = []
	for acp in wdev.GetAllAccessPoints():
		info = {}
		for attr_i in attr_interest:
			info[attr_i] = getattr(acp,attr_i)
		info['Channel'] = channel[info['Frequency']]
		#print(info)
		ap_info.append(info)
	return ap_info

def create_connProfile(ssid,bssid="",user="",password=""):
	"""Function used to create a new connection profile.

	:param ssid: is the ssid of the access point.
	:type ssid: str

	:returns: A dictionary with all the information necessary to create a connection profile
	:rtype: dict
	"""
	conn = {}
	conn['connection'] = {
		'autoconnect' : False,
		'type': '802-11-wireless', 
		'uuid': str(uuid.uuid4())}
		
	conn['802-11-wireless'] = {
			'mac-address-blacklist': [],
			'mode': 'infrastructure', 
			'security': '802-11-wireless-security'}
			
	conn['ipv4'] = {'method': 'auto'}
	conn['ipv6'] = {'method': 'auto'}
	
	fbssid = bssid.replace(":","_")
	
	conn['802-11-wireless']['ssid'] = ssid
	
	if bssid == "":
		conn['connection']['id'] = ssid
	else:
		conn['connection']['id'] = fbssid
		conn['802-11-wireless']['bssid'] = bssid
		
	if user != "":
		conn['802-11-wireless-security'] = {
				'key-mgmt': 'wpa-eap'}
		
		conn['802-1x'] = {
			'eap': ['peap'], 
			'identity': user, 
			'password': password,
			'phase2-auth': 'mschapv2'}
	elif password != "":
		conn['802-11-wireless-security'] = {
				'key-mgmt': 'wpa-psk',
				'psk': password}
	return conn
	

def connecttoAP(ssid,bssid="",user="",password="",timeout=-1):
	"""This functions try to connect to a network with the given parameters
	
	Currently this function can only connecto to:
	
	* open networks
	* psk tkip networks
	* peap mschapv2 networks

	this function prioritizes ssid over bssid
	always return the bssid of the network connected to

	:param ssid: is the ssid of the access point to connect to
	:type ssid: str
	:param timeout: is the numbers of seconds to wait for connection, -1 for wait until connect
	:type timeout: int

	:returns: False if the connection failed or a string with the MacAddress
	:rtype: bool|str
	"""
	acpoints =[]
	deactive_wireless_conn()
	if ssid != "":
		acpoints,wdev = accessPoints('Ssid',ssid)
	elif bssid != "":
		acpoints,wdev = accessPoints('HwAddress',bssid)
	if acpoints != []:
		if ssid != "":
			conn = connectProfile('802-11-wireless','ssid',ssid)
		elif bssid != "":
			ssid = acpoints[0].Ssid
			fbssid = bssid.replace(":","_")
			conn = connectProfile('802-11-wireless','bssid',bssid)
		else:
			return False
			
		if conn == None:
			conn_s = create_connProfile(ssid,bssid=bssid,user=user,password=password)
			conn = NetworkManager.Settings.AddConnection(conn_s)
			
		x = nm.ActivateConnection(conn, wdev, "/")
		#print(type(x))
		time_elapse = 0
		time_delta = 1
		
		while wdev.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED and (time_elapse < timeout or timeout == -1):
			time_elapse += time_delta
			#print("no connected",time_elapse)
			time.sleep(time_delta)
		if(wdev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED):
			return wdev.ActiveAccessPoint.HwAddress
		
			
	return False
			
		


def connectMAC(bssid,user="",password=""):
	"""This functions try to connect to a network with the given bssid(MacAddress)
	
	Currently this function can only connecto to:

	* open networks
	* psk tkip networks
	* peap mschapv2 networks

	this function prioritizes ssid over bssid
	always return the bssid of the network connected to

	:param bssid: is the bssid(MacAddress) of the access point to connect to
	:type bssid: str

	:returns: False if the connection failed or a string with the MacAddress
	:rtype: bool|str
	"""
	return connecttoAP(ssid="",bssid=bssid,user=user,password=password)

def JaverianaCali(user,password):
	"""Function used to connect to the network JaverianaCali with the given user and password.

	Is assumed that JaverianaCali is an 802.1x connection. This function is only for test, 
	use connecttoAP instead.

	:param user: is a string with a valid user
	:type user: str
	:param password: is a string with the password of the user
	:type password: str
	"""
	deactive_wireless_conn()
	acpoints,wdev = accessPoints('Ssid','JaverianaCali')
	if acpoints != []:
		conn = connectProfile('802-11-wireless','ssid','JaverianaCali')
		if conn != None:
			conn_s = conn.GetSettings()
			conn_s['802-1x']['identity'] = user
			conn_s['802-1x']['password'] = password
			conn.Update(conn_s)
		else:
			conn_s = {
			'connection':
				{
				'id': 'JaverianaCali', 
				'type': '802-11-wireless', 
				'uuid': str(uuid.uuid4())}, 
			'802-11-wireless-security': 
				{
				'key-mgmt': 'wpa-eap'}, 
			'802-11-wireless': 
				{
				'mac-address-blacklist': [], 
				'mode': 'infrastructure', 
				'security': '802-11-wireless-security',
				'ssid': 'JaverianaCali'}, 
			'802-1x': 
				{
				'eap': ['peap'], 
				'identity': user, 
				'password': password,
				'phase2-auth': 'mschapv2'}, 
			'ipv4': {'method': 'auto'}, 
			'ipv6': {'method': 'auto'}
			}
			conn = NetworkManager.Settings.AddConnection(conn_s)
		nm.ActivateConnection(conn, wdev, "/")

def Invitados_JaverianaCali():
	"""Function used to connect to the network 'Invitados JaverianaCali'.

	Is assumed that Invitados JaverianaCali is open. This function is only for test, 
	use connecttoAP instead.

	:param user: is a string with a valid user
	:type user: str
	:param password: is a string with the password of the user
	:type password: str
	"""
	deactive_wireless_conn()
	acpoints,wdev = accessPoints('Ssid','Invitados JaverianaCali')
	if acpoints != []:
		conn = connectProfile('802-11-wireless','ssid','Invitados JaverianaCali')
		if conn == None:
			conn_s = {
			'connection':
				{
				'id': 'Invitados JaverianaCali', 
				'type': '802-11-wireless', 
				'uuid': str(uuid.uuid4())}, 
			'802-11-wireless': 
				{
				'mode': 'infrastructure', 
				'ssid': 'Invitados JaverianaCali'}, 
			'ipv4': {'method': 'auto'}, 
			'ipv6': {'method': 'auto'}
			}
			conn = NetworkManager.Settings.AddConnection(conn_s)
		nm.ActivateConnection(conn, wdev, "/")
		
def test1():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	Invitados_JaverianaCali()
	#JaverianaCali('user','password')
	print("Finish")

def test2():
	command = input("Enter a command [press enter to stop]: ")
	while command:
			print(dir())
			command = input("Enter a command [press enter to stop]: ")

def test0():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP('HOME-A83F',password="vmcv1234"))
	print("Finish")

def testb0():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP("",bssid="CC:35:40:98:A8:3F",password="vmcv1234"))
	print("Finish")

def test01():
	password = "password"
	user = "user"
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP('JaverianaCali',password=password,user=user))
	print("Finish")

def test02():
	print("Disconnect")
	deactive_wireless_conn()
	input("Press enter to continue...")
	print("Connecting")
	print(connecttoAP('Invitados JaverianaCali'))
	print("Finish")

if __name__ == "__main__":
	test0()