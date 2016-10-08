#@author: Varoon
#This script is meant to listen to the twitch stream from hot_glue_from_purdue, interact with the
#players in the stream, and send the "consensus" of the players to an arduino to control remote cars.
# This will also assign and maintain teams.
import socket
import time
import re
import serial
import struct
import random
from sys import exit


# returns 0 if no inputs from twitch. Otherwise outputs distinct value for each cardinal and intercardinal
# direction. All values between 0 and 10, inclusive. Powers of two guarantee distinctiveness under addition
def get_mvmt_val(team):
    for i in commands[team]:
        if i!=0:
            return 2**(commands[team].index(max(commands[team][0:2])))+2**(2+commands[team][2:4].index(max(commands[team][2:4])))
    return 0

HOST = "irc.twitch.tv"
PORT = 6667

#FOR SIMPLICITY, 0=RED_TEAM, 1=BLUE TEAM
teams={0:'Red',1:'Blue'}
#From the moderator channel
NICK = "twitchplaysbattlebots"
PASS = "oauth:0dyincbnyg1swo4y4eirxn6iczixdo"

#From the streamer channel
CHAN = "#twitchplaysbattlebots"

current_time = time.time()
ser = serial.Serial('/dev/ttyACM3',9600)

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


    a = get_mvmt_val(0)
    b = get_mvmt_val(1)

    print(str(a) + "," + str(b))
    ser.write(struct.pack('>BB', a, b))
        #commands=[[0,0,0,0],[0,0,0,0]]      #resets commands list


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
                s.send('PRIVMSG %s :%s\r\n' % (CHAN, '{} is now on the {} Team'.format(username, teams.get(0).encode('utf-8'))))
            elif numBlue<numRed:
                registered_users[username]=1
                numBlue+=1
                s.send('PRIVMSG %s :%s\r\n' % (CHAN, '{} is now on the {} Team'.format(username, teams.get(1).encode('utf-8'))))

            else:

                if random.randint(0,1)==0:
                    registered_users[username]=0
                    numRed+=1
                    s.send('PRIVMSG %s :%s\r\n' % (CHAN, '{} is now on the {} Team'.format(username, teams.get(0).encode('utf-8'))))

                else:
                    registered_users[username]=1
                    numBlue+=1
                    s.send('PRIVMSG %s :%s\r\n' % (CHAN, '{} is now on the {} Team'.format(username, teams.get(1).encode('utf-8'))))

        else: #if the user is registered
            if registered_users.has_key(username):
                message = CHAT_MSG.sub("",line).rstrip()

                    #increments commands list if possible
                try:
                    if message == "stop":
                        quit('stopped by user')
                    else:
                        commands[registered_users.get(username)][command_lookup.get(message,0)]+=1

                except:
                    s.send('PRIVMSG %s :%s\r\n' % (CHAN, '{} has an invalid entry. Remember, only enter f,b,l,or r.\n'.format(username).encode('utf-8')))
