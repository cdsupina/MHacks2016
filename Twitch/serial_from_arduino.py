import socket
import time
import re
import random
import mvmt_val
import serial
import struct

ser = serial.Serial('/dev/ttyACM2',9600)
while True:
    data = ser.readline()[:-2]
    if data:
        print(data)
