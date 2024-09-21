import string
import scapy.all as scapy
import re

'''
ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

while True:
    ip_add_range_entered = input("\Enter IP range")
    if ip_add_range_pattern.search(ip_add_range_entered):
        print(f"{ip_add_range_entered} is a valid address range")
        break

arp_result = scapy.arping(ip_add_range_entered)
#print(f"result type{type(arp_result)}, result 1 : {arp_result[1]}")

wlan0 = scapy.get_if_hwaddr("wlan0")
eth0 = scapy.get_if_hwaddr("eth0") '''

def find_raspi(network_list) ->list:
    #search mac addresses
    address_list = ['b8:27:eb', 'dc:a6:32', 'd8:3a:dd']
    broadcom = "B8:27:EB"
    common = "DC:A6:32"
    pi_list = []

    for device in devices:
        for mac in address_list:
            if mac in device['mac']:
                print(device['ip'])
                pi_list.append(device['ip'])

    return pi_list


    

from scapy.all import arping

# Define the network range (replace with your network range if needed)
ip_range = "192.168.100.0/24"

# Perform the ARP scan
arp_result = arping(ip_range, timeout=2, verbose=False)[0]

# Create a list to store IP and MAC address pairs
devices = []

# Extract IP and MAC addresses and store them in the list
for sent, received in arp_result:
    devices.append({'ip': received.psrc, 'mac': received.hwsrc})

find_raspi(devices)



# Print the list of devices
print("Devices on the network:")
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")

'''
    Raspi chips are manufactured by broadcom and  common OUI
    B8:27:EB
    DC:A6:32
    E4:5F:01
'''