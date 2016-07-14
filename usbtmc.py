#!/usr/bin/env python3 -u

# This file is a copy of https://github.com/sbrinkmann/PyOscilloskop/blob/master/src/usbtmc.py


#To find VENDER_ID and PRODUCT_ID execute $dmesg | grep usb, look for values
#called idvendor and idProduct right above an entry saying "Rigol"

#https://github.com/python-ivi/python-usbtmc/blob/master/usbtmc/usbtmc.py
#^Link to usbtmc library with much more functionality than mine.
#Also got the permision fix from him.
#To get rid of the permissions error: http://alexforencich.com/wiki/en/python-usbtmc/readme
#If you cannot access your device without running your script as root, then you may need to create a udev rule to properly set the permissions of the device. First, connect your device and run lsusb. Find the vendor and product IDs. Then, create a file /etc/udev/rules.d/usbtmc.rules with the following content:
#      USBTMC instruments
#       Agilent MSO7104
#      SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="0957", ATTRS{idProduct}=="1755", GROUP="usbtmc", MODE="0660"
#substituting the correct idVendor and idProduct from lsusb. You will also need to create the usbtmc group and add yourself to it or substitute another group of your choosing. It seems that udev does not allow 0666 rules, usually overriding the mode to 0664, so you will need to be a member of the associated group to use the device.



#The groupadd command can be used in Linux to add user groups to the system. The basic syntax of Linux groupadd command is groupadd <groupname>. If no command-line options are used, the group is created with the next available Group ID number (GID) above 499. To specify a GID, use the groupadd -g <gid> <group-name> command.
#[root@RHEL2 ~]# groupadd engineering
#To add existing Linux users to a group, use the usermod -aG <groups> <username> command.
#[root@RHEL2 ~]# usermod -aG engineering tintin
#Note: You should be familiar how to add a user in Linux before learning this lesson. Click the following link to learn how to add a user in a Linux machine using useradd command.


import os
import time

class usb_instrument:
    """Simple implementation of a USBTMC device driver, in the style of visa.h"""

    def __init__(self, device=None):
        if device == None: self.device = getDeviceList()[-1]
        else: self.device = device
        self.FILE = open( bytes(self.device, 'UTF-8'), 'w+b', buffering=0)


        print( self.getName())

        # TODO: Test that the file opened

    def write(self, command):
        self.FILE.write(bytes(command, 'UTF-8'));


    def read(self, length = 4000, quick=False):
        #Will go much faster if you know how many bytes to read
        # :WAV:DATA? on NORM setting: length =1211
        t = ''
        try:
            if quick: return self.FILE.read(length)
            t = self.FILE.read(1)
            try:
                for i in range(1,length):
                    t = t + self.FILE.read(1)
            except: None
        except:
            print("No Values in Buffer")
        self.FILE.flush()
        return t

    def read_all(self):
        t = ''
        try:
            t = self.FILE.read(1)
            try:
                while(True):
                    t = t + self.FILE.read(1)
            except: None
        except:
            print("No Values in Buffer")
            t=-1
        self.FILE.flush()
        return t

    def ask(self, command, length=None):
        self.write(command);
        if length is not None: return self.read(length, True)
        time.sleep(1) #Give scope a chance to respond
        return self.read_all();

    def getName(self):
        self.write("*IDN?")
        return self.read(300,quick=True)

    def sendReset(self):
        self.write("*RST")

    def sample_max(self, channel):
        print("Sampling with Maximum Resolution...")
        collected_sample = None
        self.write(":WAV:POIN:MODE MAX")
        while(True):
            self.write(":WAV:DATA? "+ channel)
            buff = self.read_all()
            if(buff==-1):
                print("... sample collected. " +str(len(collected_sample)) + " data points captured." )
                return collected_sample
            if(collected_sample == None): collected_sample = buff
            else: collected_sample = collected_sample + buff
            print("Datapoints Captured: " + str( len(collected_sample)))
            time.sleep(1)
    def sample_norm(self, channel):
        self.write(":WAV:POIN:MODE NORM")
        self.write(":WAV:DATA? "+ channel)
        return self.read(1211)



def getDeviceList():
    dirList=os.listdir("/dev")
    result=list()

    for fname in dirList:
        if(fname.startswith("usbtmc")):
            result.append("/dev/" + fname)

    return result
