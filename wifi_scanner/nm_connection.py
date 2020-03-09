import NetworkManager
import uuid
import time
#ConectarMac
#ConectarInvJave
#JaverianaCali

#timeout 5s [tiempo promedio de conexion, retornar cuando pase el timeout]
#sincrono

#funcion que retorne directorio con esos parametros, documentar los pasos
#ssid
#db
#hwmac
#channel
#frecuencia [canal]

nm = NetworkManager.NetworkManager

def accessPoints(prop,value):
    #prop is the property that must have an access point of interest
    #value is the respective value that property must have
    
    devices = nm.GetAllDevices()
    wdev = None
    for dev in devices:
        if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
            wdev = dev
            break
    acpoints = []
    for acp in wdev.GetAllAccessPoints():
        acp_attr = dir(acp)

        if prop in acp_attr and getattr(acp,prop) == value:
            acpoints.append(acp)
    return (acpoints,wdev)

def connectProfile(setting, key, value):
    #setting is the setting that must have a connection profile
    #key is the respective value that property must have
    connections = NetworkManager.Settings.ListConnections()
    for conn in connections:
        conn_s = conn.GetSettings()
        if setting in conn_s and key in conn_s[setting] and value == conn_s[setting][key]:
            return conn

def deactive_wireless_conn():
    for aconn in nm.ActiveConnections:
        if aconn.Type == '802-11-wireless':
            nm.DeactivateConnection(aconn)
    time.sleep(4)

#HwAddress is the MAC address or BSSID of the AP
#Strength is the strength of the AP signal in percent
#Frequency is the frequency band of the AP in MHz
attr_interest = ['Ssid','HwAddress','Strength','Frequency']
channel = dict([(2407+5*i,i) for i in range(1,14)])
channel[2484] = 14

channel_5G = dict([(5000+5*i,i) for i in range(1,200)])
def get_all_ap_info():
    #this function disconnects NetworkManager from the AP
    deactive_wireless_conn()
    devices = nm.GetAllDevices()
    wdev = None
    for dev in devices:
        if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
            wdev = dev
            break
    ap_info = []
    #print(wdev.GetAllAccessPoints())
    for acp in wdev.GetAllAccessPoints():
        info = {}
        for attr_i in attr_interest:
            info[attr_i] = getattr(acp,attr_i)
        if info['Frequency'] in channel:
            info['Channel'] = channel[info['Frequency']]
        elif info['Frequency'] in channel_5G:
            info['Channel'] = channel_5G[info['Frequency']]
        else:
            info['Channel'] =  info['Frequency']
        #print(info)
        ap_info.append(info)
    return ap_info

def create_connProfile(ssid,bssid="",user="",password="",autoconnect=False, autoc_priority=0):
    conn = {}
    conn['connection'] = {
        'autoconnect' : autoconnect,
        'autoconnect-priority':autoc_priority,
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
    if ssid=="":
        conn['802-11-wireless']['hidden'] = True
    
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
    

def connecttoAP(ssid,bssid="",user="",password="",timeout=-1,autoconnect=False, autoc_priority=0):
    """This functions try to connect to a network with the given parameters
    
    Currently this function can only connecto to:
        -open networks
        -psk tkip networks
        -peap mschapv2 networks
    this function prioritizes ssid over bssid
    always return the bssid connected to.
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
            conn_s = create_connProfile(ssid,bssid=bssid,user=user,password=password, autoconnect=autoconnect, autoc_priority=autoc_priority)
            print(conn_s)
            conn = NetworkManager.Settings.AddConnection(conn_s)
            
        x = nm.ActivateConnection(conn, wdev, "/")
        time_elapse = 0
        time_delta = 1
        
        while wdev.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED and (time_elapse < timeout or timeout == -1):
            time_elapse += time_delta
            #print("no connected",time_elapse)
            time.sleep(time_delta)
        if(wdev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED):
            return wdev.ActiveAccessPoint.HwAddress
        
            
    return False
    
def JaverianaCali(user,password,timeout=-1,autoconnect=False, autoc_priority=100):
    """This function tries to connect to a network with ssid=JaverianaCali
    and assumes that the AP use wpa2-eap connection with user and password
    as login credentials
    
    user and password are strings. return a string with de MACaddress of 
    the AP.
    """
    return connecttoAP('JaverianaCali',password=password,user=user,timeout=timeout,autoconnect=autoconnect, autoc_priority=autoc_priority)

def Invitados_JaverianaCali():
    """This function tries to connect to a network with ssid="Invitados JaverianaCali"
    and assumes that the AP doesn't have security
    
    return a string with the MACaddress of the AP.
    """
    return connecttoAP('Invitados JaverianaCali')
    

def JaverianaCali_backup(user,password):
    #is assumed that JaverianaCali is an 802.1x connection
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

def Invitados_JaverianaCali_backup():
    #is assumed that Invitados JaverianaCali is open
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
        

