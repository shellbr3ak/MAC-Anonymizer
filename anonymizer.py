#!/usr/bin/env python3

import argparse
import os
import subprocess
import random
from apscheduler.schedulers.blocking import BlockingScheduler
from colorama import Fore

def anonymize(interface,):
    new_mac = generate()
    print(f'Your new MAC address is {Fore.GREEN}{new_mac}{Fore.WHITE}')
    subprocess.call(f'ifconfig {interface} down', shell=True)
    subprocess.call(f'ifconfig {interface} hw ether {new_mac}', shell=True)
    subprocess.call(f'ifconfig {interface} up', shell=True)

def generate():
    valid_chars = '0123456789abcdef'
    combos = ['12']
    for i in range(5):
        combo = valid_chars[random.randint(0, 15)] + valid_chars[random.randint(0, 15)]
        combos.append(combo)
    return ':'.join(combos)


def check_iface(interface):
    ifaces = os.listdir('/sys/class/net/')
    if interface not in ifaces:
        return False
    else:
        return True

try :

    parser = argparse.ArgumentParser(description="Usage: sudo python3 macchanger.py -i <INTERFACE>")
    parser.add_argument('-i', dest="interface", help="Interface of which you want to change the mac address")
    parser.add_argument('-t', dest="time", help="The Time after which a new mac address will be generated and assigned <minutes>")
    parsed_args = parser.parse_args()
    
    if(check_iface(parsed_args.interface)):
        old_mac_address = subprocess.check_output("ifconfig " + parsed_args.interface + "|grep ether| awk '{print $2}'", shell=True).decode().strip()
        print(f'Your current MAC address is: {Fore.BLUE}{old_mac_address}{Fore.WHITE}')
        sched = BlockingScheduler()
        sched.add_job(anonymize, "interval", [parsed_args.interface], minutes = int(parsed_args.time))
        anonymize(parsed_args.interface)
        sched.start()

    else:
        print(f'{Fore.YELLOW}No Such Interface{Fore.WHITE}')

except KeyboardInterrupt:
    print(f'{Fore.RED}Script Terminated{Fore.WHITE}')
except :
    print(f'{Fore.YELLOW}{parser.description}{Fore.WHITE}')
