import re
import subprocess
import json
from datetime import datetime
import wifi_scanner.config as config
from os import listdir,remove
import time

cellNumberRe = re.compile(r"Address:\s(?P<mac_ssid>.+)$")
regexps = [
    re.compile(r"^ESSID:\"(?P<ssid>.*)\"$"),
    #Frequency:2.437 GHz (Channel 6)
    re.compile(r"^Frequency:(?P<frequency>[\d.]+)\s+GHz\s+\(Channel (?P<channel>\d+)\)$"),
    re.compile(r"Signal level=(?P<signal_level_dBm>.+) d.+$"),
]
rasp_mac = re.compile(r"link/ether\s+(?P<rasp_mac>(([a-z0-9]){2}:)+([a-z0-9]){2})")

# Runs the comnmand to scan the list of networks.
# Must run as super user.
def get_command_output(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.read().decode('utf-8')

def scan(interface='wlan0'):
    cmd = ["iwlist", interface, "scan"]
    return get_command_output(cmd)

def interface_info(interface='wlan0'):
    cmd = ["ip", "link", "show",interface]
    return get_command_output(cmd)

def get_datetime_str():
    return datetime.now().strftime(config.datetime_format)

# Parses the response from the command "iwlist scan"
def parse(content,macaddr="01:02:03:04:05:06"):
    cells = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        cellNumber = cellNumberRe.search(line)
        if cellNumber is not None:
            cells.append(cellNumber.groupdict())
            cells[-1].update({"datetime":get_datetime_str()})
            cells[-1].update({"dev_mac":macaddr})
            continue
        for expression in regexps:
            result = expression.search(line)
            if result is not None:
                cells[-1].update(result.groupdict())
                continue
    return cells

def send_data_to_server(jsonStr):
    return True

def main():
    #Get MAC of the current device
    macaddr = None
    for line in interface_info().split("\n"):
        result = rasp_mac.search(line)
        if result is not None:
            macaddr=result.groupdict()
            break
    #Get the data that is pending for send
    pending = [f for f in listdir(config.files_path) if f.split(".")[-1] == "json"]
    total_time = 0
    while True:
        if total_time>config.sample_time:
            total_time = 0
            
        if total_time == 0:
            print("scanning")
            jsonStr = json.dumps(parse(scan(interface='wlan0')))
            if send_data_to_server(jsonStr) == None:
                file_name = get_datetime_str()+".json"
                with open(config.files_path+"/"+file_name,"w+") as f:
                    f.write(jsonStr)
                pending.append(file_name)
        if pending:
            sended = True
            print("sending pending data")
            while (sended != None) and pending:
                file_name = pending[-1]
                with open(config.files_path+"/"+file_name,"r") as f:
                    jsonStr = f.read()
                    sended = send_data_to_server(jsonStr)
                if sended != None:
                    print(file_name+" sended")
                    remove(config.files_path+"/"+file_name)
                    pending.pop()
        if pending:
            print("waiting to send pending data")
            print(pending)
            total_time += config.reconnect_time
            time.sleep(config.reconnect_time)
        else:
            print("no pending")
            time.sleep(config.sample_time-total_time)
            total_time += config.sample_time

main()

#with open(config.files_path+"/prueba.json","w+") as f:
#    json.dump(parse(scan(interface='wlan0')),f)
#with open(config.files_path+"/prueba.json","r") as f:
#    print(f.read())
#for e in parse(scan(interface='wlan0')):
#    print(json.dumps(e))
