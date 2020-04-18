#!/bin/sh

# This script sets the hostname to a codename based on the CPU serial number, Ethernet MAC address, and WLAN mac address

ETH=$(cat /sys/class/net/eth0/address)
WLAN=$(cat /sys/class/net/wlan0/address)
SERIAL=$(cat /proc/cpuinfo  | grep Serial | cut -d: -f2)
HOSTNAME=$(codenamize -p 2 -a sha3_512 -m 0 ${SERIAL}-${ETH}-${WLAN})
echo Setting hostname to ${HOSTNAME}
hostnamectl set-hostname ${HOSTNAME}
