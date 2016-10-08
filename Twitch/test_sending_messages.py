#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 06:07:12 2016

@author: Varoon
"""

import socket
import re
import time

HOST = "irc.twitch.tv"
PORT = 6667

#From the moderator channel
NICK = "sumobotsteamred"
PASS = "oauth:6cp3so6qpa1rqwdy1bva9nqu0deswg"

#From the streamer channel
CHAN = "#hot_glue_from_purdue"



s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
messages=['hello','this message is from a bot','eh']
for message in messages:
    s.send('PRIVMSG %s :%s\r\n' % (CHAN, message.encode('utf-8')))
    time.sleep(4)