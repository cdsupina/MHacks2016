import socket
import time
import re
import serial
import struct

HOST = "irc.twitch.tv"
PORT = 6667

#From the moderator channel
NICK = "sumobotsteamred"
PASS = "oauth:6cp3so6qpa1rqwdy1bva9nqu0deswg"

#From the streamer channel
CHAN = "#hot_glue_from_purdue"

#ser = serial.Serial('/dev/ttyACM0',9600)

#viewers need to register for one of two teams
registered_users = {}


CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

while True:
    line = s.recv(1024).decode("utf-8")
    if line == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+",line).group(0)
        message = CHAT_MSG.sub("",line).rstrip()
        message_split = message.split('-')
        if message_split[0] == "register":
            registered_users[username] = "registered"

        print(username + ": " + message)
        print(registered_users)
