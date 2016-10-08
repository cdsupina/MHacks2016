#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 04:16:46 2016

@author: Varoon
"""

import socket
import time
import re
import serial
import struct
import random

#sends 2 bytes from the list of possibilites every second.
poss=[0,1,2,4,8,5,9,6,10]
ser = serial.Serial('/dev/ttyACM0',9600)
while True:
    time.sleep(1)
    ser.write('>BB',poss[random.randrange(0,7)], poss[random.randrange(0,7)])