#///!/usr/bin/env ///////python3 -u

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
import usbtmc
import usb
import usb.core

class usb_instrument:
    
	
    def __init__(self, idVendor, idProduct):
	self.device = usbtmc.Instrument(idVendor,idProduct)

    def write(self, command):
        self.device.write(command.encode('UTF-8'));

    def read(self, length = 4000, blockSize = 1, quick=False):
        #Will go much faster if you know how many bytes to read
        # :WAV:DATA? on NORM setting: length =1211
        t = ''	
        try:
            if quick: return self.read(length)
            t = self.device.read(blockSize)
            try:
                for i in range(1,length/blockSize):
                    t = t + self.device.read(blockSize)
            except: raise 
        except USBError:
            print("No Values in Buffer")
	    return -1
        return t

    def read_all(self, attempts=5):
        t = ''
        try:
            t = self.device.read(1)
	    t = t+ self.device.read(1)
	    for tempt in range(0,attempts):	
		    try:
		        while(True):
		            t = t + self.device.read(1)
		    except: None
        except: 
	    raise
            print("No Values in Buffer")
            t=-1
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



