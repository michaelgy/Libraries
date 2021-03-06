#!/usr/bin/python3
#Run as sudo for complete AP list
import re
import wifi_scanner.config as config
from os import listdir,remove
import wifi_scan_common_tools as wctools
import json
import requests, traceback

#falta ssid
reg_list = [
    re.compile(r"Address:\s(?P<ssidMac>.+)$"),
    re.compile(r"^Frequency:(?P<bandaFrecuencia>[\d.]+)\s+GHz\s+\(Channel (?P<canal>\d+)\)$"),
    re.compile(r"Signal level=(?P<dbm>.+) d.+$"),
    re.compile(r"^ESSID:\"(?P<ssidNombre>.*)\"$")
]

macaddr = wctools.get_macaddr()

def parse(content,reg_list,additional_info={}):
    """parse the output of a cmd output in to a dictionary of tokens
"""
    cells = []
    i = 0
    for line in content.split('\n'):
        sres  = reg_list[i].search(line.strip())
        if sres is not None:
            if i==0:
                cells.append(sres.groupdict())
                cells[-1].update(additional_info)
            else:
                cells[-1].update(sres.groupdict())
            i = (i+1)%len(reg_list)
    return cells

def scan(interface='wlan0'):
    content = wctools.get_command_output("iwlist {} scan".format(interface))
    additional_info={
        "fecha":wctools.get_datetime_str(config.datetime_format_data),
        "macDispositivo":macaddr,
        "ubicacion":config.ubicacion
    }
    cells = parse(content,reg_list,additional_info=additional_info)
    return cells

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

wctools.main(init_f, init_args, main_f, main_args, pend_f, pend_args, config, debug = False)