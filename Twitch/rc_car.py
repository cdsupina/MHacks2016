import socket
import time
import re
import serial
import struct
import datetime
import time
import random

HOST = "irc.twitch.tv"
PORT = 6667

#FOR SIMPLICITY, 0=RED_TEAM, 1=BLUE TEAM
#From the moderator channel
NICK = "sumobotsteamred"
PASS = "oauth:6cp3so6qpa1rqwdy1bva9nqu0deswg"
print 'hello'
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

while True:
    if time.time()-current_time>1:
        print[2**(commands[0].index(max(commands[0][0:2])))+2**(commands[0].index(max(commands[0][2:4]))) 
            ,2**(commands[1].index(max(commands[1][0:2])))+2**(commands[1].index(max(commands[1][2:4])))]
        #ser.write(struct.pack('>BB',2**(commands[0].index(max(commands[0][0:2])))+2**(commands[0].index(max(commands[0][2:4]))) 
        #    ,2**(commands[1].index(max(commands[1][0:2])))+2**(commands[1].index(max(commands[1][2:4])))))
        current_time=time.time()
        commands=[[0,0,0,0],[0,0,0,0]]
    else:
        line = s.recv(1024).decode("utf-8")
        if line == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+",line).group(0)
            
            # if user is not registered
            if not registered_users.has_key(username):
                if numRed<numBlue:
                    registered_users[username]=0
                    numRed+=1
                elif numBlue<numRed:
                    registered_users[username]=1
                    numBlue+=1
                else:
                    
                    if random.randint(0,1):
                        registered_users[username]=0
                        numRed+=1
                    else:
                        registered_users[username]=1
                        numBlue+=1
            else: #if the user is registered
                if registered_users.has_key(username):
                    message = CHAT_MSG.sub("",line).rstrip()
                    
                    #increments commands list if possible
                    try:
                        commands[registered_users.get(username)][command_lookup.get(message,0)]+=1
                    except:
                        print 'There was an error. Send this in the twitch chat.'
                
               
                        
    
            
