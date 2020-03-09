import re
import wifi_aptest.config as config
from os import listdir,remove
import wifi_scan_common_tools as wctools
import json
import requests, traceback

#falta ssid
reg_list = [
    re.compile(r"^\d+\s+packets transmitted,\s+\d+\s+received,\s+(?P<loss>[\d+\.]+)\% packet loss,\s+time \d+ms"),
    re.compile(r"^rtt min/avg/max/mdev = (?P<minv>[\d\.]+)/(?P<avgv>[\d\.]+)/(?P<maxv>[\d\.]+)")
]

macaddr = wctools.get_macaddr()

def parse(content,reg_list,additional_info={}):
    """parse the output of a cmd output in to a dictionary of tokens
"""
    info = {}
    i = 0
    for line in content.split('\n'):
        sres  = reg_list[i].search(line.strip())
        if sres is not None:
            i=(i+1)%len(reg_list)
            info.update(sres.groupdict())
    return info

url = "www.google.com"
def scan(interface='wlan0'):
    cmd = "ping -c {count} -i {interval} -I {interface} -W {timeout} -w {deadline} {url}"
    params = {
        "count":config.count,
        "interval":config.interval,
        "interface":interface,
        "timeout":config.timeout,
        "deadline":config.deadline,
        "url":url}
    content = wctools.get_command_output(cmd.format(**params))
    additional_info={
        "fecha":wctools.get_datetime_str(config.datetime_format_data),
        "macDispositivo":macaddr,
    } #falta macssid, dbm, conexion exitosa, direccionweb
    cells = parse(content,reg_list,additional_info=additional_info)
    return cells
print(scan())
            
def save_data(remain):
    file_name = wctools.get_datetime_str(config.datetime_format_file)+".json"
    with open(config.files_path+"/"+file_name,"w+") as f:
        f.write(json.dumps(remain))
    return file_name

def send_data_to_server(listDict):
    while listDict:
        jsdict = listDict.pop()
        try:
            r = requests.post(config.url_servicio,json=jsdict)
            if r.status_code != 200:
                listDict.append(jsdict)
                break
        except requests.exceptions.ConnectionError as connErr:
            listDict.append(jsdict)
            break
        except Exception as err:
            print(traceback.format_exc())
            listDict.append(jsdict)
            break
        
    return listDict

def init_f():
    return
init_args = ()

def main_f(pending):
    print(pending)
    print("scanning")
    jsonList = scan()
    remain = send_data_to_server(jsonList)
    if remain:
        file_name = save_data(remain)
        pending.append(file_name)
main_args = ()

def pend_f(pending):
    remain = False
    print("sending pending data")
    print(pending)
    while (not remain) and pending:
        file_name = pending.pop()
        with open(config.files_path+"/"+file_name,"r") as f:
            jsonList = json.loads(f.read())
            remain = send_data_to_server(jsonList)
        if not remain:
            print(file_name+" was sended")
        else:
            print(file_name, " remain data was not sended")
            file_name_remain = save_data(remain)
            pending.append(file_name_remain)
            print(file_name_remain)
        
        remove(config.files_path+"/"+file_name)
pend_args = ()

#wctools.main(init_f, init_args, main_f, main_args, pend_f, pend_args, config, debug = False)
