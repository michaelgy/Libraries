import subprocess
from datetime import datetime
import re
import time
from os import listdir

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

def main(init_f, init_args, main_f, main_args, pend_f, pend_args, config, debug = False):
    #call to the init function
    init_f(*init_args)
    #Get the data that is pending for send
    pending = [f for f in listdir(config.files_path) if f.split(".")[-1] == config.data_file_ext]
    total_time = 0
    while True:
        if total_time>=config.sample_time:
            total_time = 0
            
        if total_time == 0:
            main_f(pending, *main_args)
                
        if pending:
            pend_f(pending, *pend_args)
            
        if pending:
            if debug:
                print("waiting to send pending data")
            total_time += config.reconnect_time
            time.sleep(config.reconnect_time)
        else:
            if debug:
                print("no pending")
            time.sleep(config.sample_time-total_time)
            total_time += config.sample_time