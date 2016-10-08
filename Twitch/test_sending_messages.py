#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 06:07:12 2016

@author: Varoon
"""

import socket
import time
import re
import serial
import struct
import random
from sys import exit

# returns 0 if no inputs from twitch. Otherwise outputs distinct value for each cardinal and intercardinal 
# direction. All values between 0 and 10, inclusive. 
def get_mvmt_val(team):    
    for i in commands[team]:
        if i!=0:
            print (commands[team].index(max(commands[team][0:2])))
            print (2+commands[team][2:4].index(max(commands[team][2:4])))
            return 2**(commands[team].index(max(commands[team][0:2])))+2**(2+commands[team][2:4].index(max(commands[team][2:4])))
    return 0

HOST = "irc.twitch.tv"
PORT = 6667

#FOR SIMPLICITY, 0=RED_TEAM, 1=BLUE TEAM
#From the moderator channel
NICK = "sumobotsteamred"
PASS = "oauth:6cp3so6qpa1rqwdy1bva9nqu0deswg"

#From the streamer channel
CHAN = "#hot_glue_from_purdue"

current_time = time.time()
#ser = serial.Serial('/dev/ttyACM0',9600)

#viewers need to register for one of two teams
registered_users = {}
numRed=0;
numBlue=0
#list of lists for commands. Red team then blue team. Forward, back, left, right
commands=[[0,0,0,0],[0,0,0,0]]
command_lookup={'f':0, 'b':1,'l':2,'r':3}
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
messages=['hello','this message is from a bot','eh']
for message in messages:
    time.sleep(3)
    s.send('PRIVMSG %s :%s\n' % (CHAN, message.encode('utf-8')))