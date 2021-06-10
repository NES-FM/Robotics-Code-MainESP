# This file is executed on every boot (including wake-boot from deepsleep) aka changed

import network
import time
import machine
from modules import i2c_slave_addresses as i2csl
import sys
from modules.secrets import *
from modules.pins import pins
sys.path[1] = '/flash/lib'


if __name__ == "__main__":
    # Setup some used Variables
    i2c_master = machine.I2C(id=0, mode=machine.I2C.MASTER, speed=400000, sda=pins["Sda-Master"], scl=pins["Scl-Master"])
    # i2c_slave = machine.I2C(id=1, mode=machine.I2C.SLAVE, speed=400000, sda=pins["Sda-Cam"], scl=pins["Scl-Cam"], slave_addr=i2csl.addr_addr)

    WLAN_USED_SSID = "None"
    WLAN_USED_PASSWD = "None"

    print("BOOT: Initializing Wifi")

    wlan = network.WLAN()

    if not wlan.active():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        local_wlan = wlan.scan()
        print("BOOT: [Wifi] {}".format(local_wlan))
        for ssid, pwd, ips in zip(WLAN_SSIDs, WLAN_PASSWDs, WLAN_IPSTR):
            for net in local_wlan:
                if net[0].decode("UTF-8") == ssid:
                    print("BOOT: [Wifi] Connecting to " + ssid)
                    wlan.ifconfig((ips + WLAN_IP, '255.255.255.0', ips + '1', ips + '1'))
                    wlan.connect(ssid, pwd)
                    time.sleep(6)
                    print("BOOT: [Wifi] Connected! Ip: {}".format(wlan.ifconfig()[0]))
                    WLAN_USED_SSID = ssid
                    WLAN_USED_PASSWD = pwd
                    break
            if wlan.isconnected() is True:
                break
        else:
            print("BOOT: [Wifi] Changing to AP Mode")
            wlan = network.WLAN(network.AP_IF)
            wlan.active(True)
            time.sleep(1)
            wlan.config(essid=WLAN_AP_SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=WLAN_AP_PASSWD, dhcp_hostname="main_esp")
            time.sleep(2)

    if network.ftp.status()[0] == -1:
        network.ftp.start()
    if network.telnet.status()[0] == -1:
        network.telnet.start()

"""
    print("BOOT: Setting default I2C data on slave bus")
    i2c_slave.setdata(bytearray("tl:f|tr:f|dl:f|dr:f"), i2csl.addr_cam_green)
    i2c_slave.setdata(bytearray("||+00"), i2csl.addr_cam_line)

    i2c_slave.setdata(bytearray("BUFFEREND"), i2csl.addr_bufferend)
"""
