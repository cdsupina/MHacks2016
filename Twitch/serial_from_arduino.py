import socket
import time
import re
import random
import mvmt_val
import serial
import struct

ser = serial.Serial('/dev/ttyACM1',9600)
