#!/usr/bin/python3
#Run as sudo for complete AP list
import wifi_aptest.config as config_aptest
import wifi_scanner.config as config_scanner
import config_general as config
from os import listdir,remove
import wifi_scan_common_tools as wctools
import json
import requests, traceback
import subprocess
from datetime import datetime
import re
import time
from os import listdir
import nm_connection


regex_scan = [
    re.compile(r"Address:\s(?P<ssidMac>.+)$"),
    re.compile(r"^Frequency:(?P<bandaFrecuencia>[\d.]+)\s+GHz\s+\(Channel (?P<canal>\d+)\)$"),
    re.compile(r"Signal level=(?P<dbm>.+) d.+$"),
    re.compile(r"^ESSID:\"(?P<ssidNombre>.*)\"$")
]

#falta ssid
regex_ping = [
    re.compile(r"^\d+\s+packets transmitted,\s+\d+\s+received,\s+(?P<loss>[\d\.]+)\% packet loss,\s+time \d+ms"),
    re.compile(r"^rtt min/avg/max/mdev = (?P<minv>[\d\.]+)/(?P<avgv>[\d\.]+)/(?P<maxv>[\d\.]+)")
]

macaddr = wctools.get_macaddr()

def get_command_output(cmd):
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.read().decode('utf-8')

def get_datetime_str(format_str):
    return datetime.now().strftime(format_str)

def get_macaddr(interface="eth0"):
    rasp_mac = re.compile(r"link/ether\s+(?P<rasp_mac>(([a-z0-9]){2}:)+([a-z0-9]){2})")
    macaddr = None
    cmd_out = get_command_output("ip link show {}".format(interface))
    for line in cmd_out.split("\n"):
        result = rasp_mac.search(line)
        if result is not None:
            macaddr=result.groupdict()["rasp_mac"]
            break
    return macaddr

def parse_scan(content,reg_list,additional_info={}):
    """parse the output of iwlist output in to a list of dictionary of tokens
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

def parse_ping(content,reg_list):
    """parse the output of ping output in to a dictionary of tokens
"""
    info = {}
    i = 0
    for line in content.split('\n'):
        sres  = reg_list[i].search(line.strip())
        if sres is not None:
            i=(i+1)%len(reg_list)
            info.update(sres.groupdict())
    return info

def scan(interface='wlan0'):
    content = wctools.get_command_output("iwlist {} scan".format(interface))
    additional_info={
        "fecha":wctools.get_datetime_str(config_scanner.datetime_format_data),
        "macDispositivo":macaddr,
        "ubicacion":config_scanner.ubicacion
    }
    cells = parse_scan(content,regex_scan,additional_info=additional_info)
    return cells

def ap_url_test(url,interface='wlan0'):
    cmd = "ping -c {count} -i {interval} -I {interface} -W {timeout} -w {deadline} {url}"
    params = {
        "count":config_aptest.count,
        "interval":config_aptest.interval,
        "interface":interface,
        "timeout":config_aptest.timeout,
        "deadline":config_aptest.deadline,
        "url":url}
    content = wctools.get_command_output(cmd.format(**params))
    cells = parse_ping(content,regex_ping)
    cells.update({
        "fecha":wctools.get_datetime_str(config_aptest.datetime_format_data),
        "macDispositivo":macaddr,
        "url":url
    }) #falta convertir perdidas a unidades, macssid, dbm, conexion exitosa
    return cells

def save_data(remain,config):
    file_name = wctools.get_datetime_str(config.datetime_format_file)+".json"
    with open(config.files_path+"/"+file_name,"w+") as f:
        f.write(json.dumps(remain))
    return file_name

def send_data_to_server(listDict,config):
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

def update_from_db():
    """read DB and returns a dict with the data

    The returned dict must have the following structure:
    {
        ssid1:{
            channel11:[
                url11_1,
                ...
                url11_n
                ]
            ],
            ...
            channel1n:{...}
        }
        ...
        ssidn:{...}
    }
    where ssidn is a string, channel1n is an int and
    url11_n is a string.
    """
    return {
        "JaverianaCali":{
            1:["www.google.com"]
        }
    }

def main_f(pending_scan,pending_aptest):
    targets = update_from_db()
    print("scanning")
    sc_cells = scan()
    aptest_cells = []
    print("AP testing")
    for ssid in targets:
        for channel in targets[ssid]:
            #in this step wireless connection must be performed
            for url in targets[ssid][channel]:
                aptest_cells.append(scan(url))

    remain = send_data_to_server(sc_cells,config_scanner)
    if remain:
        file_name = save_data(remain,config_scanner)
        pending_scan.append(file_name)
    remain = send_data_to_server(aptest_cells, config_scanner)
    if remain:
        file_name = save_data(remain,config_aptest)
        pending_aptest.append(file_name)

def pend_f(pending,config):
    remain = False
    print("sending pending data")
    print(pending)
    while (not remain) and pending:
        file_name = pending.pop()
        with open(config.files_path+"/"+file_name,"r") as f:
            jsonList = json.loads(f.read())
            remain = send_data_to_server(jsonList,config)
        if not remain:
            print(file_name+" was sended")
        else:
            print(file_name, " remain data was not sended")
            file_name_remain = save_data(remain,config)
            pending.append(file_name_remain)
            print(file_name_remain)
        
        remove(config.files_path+"/"+file_name)

def main():
    #Get the data that is pending for send
    pending_scan = [f for f in listdir(config_scanner.files_path) if f.split(".")[-1] == config_scanner.data_file_ext]
    pending_aptest = [f for f in listdir(config_aptest.files_path) if f.split(".")[-1] == config_aptest.data_file_ext]
    total_time = 0
    while True:
        if total_time>=config.sample_time:
            total_time = 0
            
        if total_time == 0:
            main_f(pending_scan,pending_aptest)
                
        if pending_scan:
            pend_f(pending_scan, config_scanner)
        if pending_aptest:
            pend_f(pending_aptest, config_aptest)
            
        if pending_scan or pending_aptest:
            if config.debug:
                print("waiting to send pending data")
            total_time += config.reconnect_time
            time.sleep(config.reconnect_time)
        else:
            if config.debug:
                print("no pending")
            time.sleep(config.sample_time-total_time)
            total_time += config.sample_time
