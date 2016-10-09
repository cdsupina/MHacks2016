#@author: Varoon
#This script is meant to listen to the twitch stream from hot_glue_from_purdue, interact with the
#players in the stream, and send the "consensus" of the players to the console. Mainly for testing
# This will also assign and maintain teams.
import socket
import time
import re
import random
import mvmt_val
import serial
import struct
from multiprocessing import Process
'''#gives the introductory messages to the users.

def introduction_messages():
    s.send('PRIVMSG %s :Welcome to the game!\r\n' %(CHAN))
    time.sleep(2)
    s.send('PRIVMSG %s :The rules are very simple. You will be assigned to a team that controls a car.\r\n' %(CHAN))
    time.sleep(2)
    s.send('PRIVMSG %s :Type f,b,l, or r, to go forward, backward, left, and right, respectively.\r\n' %(CHAN))
    time.sleep(2)
    s.send('PRIVMSG %s :The collective decisions of your team will decide your car\'s movement.\r\n' %(CHAN))
    time.sleep(2)
    s.send('PRIVMSG %s :The team whose car leaves the ring loses. Good Luck!\r\n' %(CHAN))
'''
def loop_a():
    HOST = "irc.twitch.tv"
    PORT = 6667

    #FOR SIMPLICITY, 0=RED_TEAM, 1=BLUE TEAM
    teams={0:'Red',1:'Blue'}
    #From the moderator channel
    NICK = "twitchplaysbattlebots"
    PASS = "oauth:0dyincbnyg1swo4y4eirxn6iczixdo"

    #From the streamer channel
    CHAN = "#twitchplaysbattlebots"

    ser = serial.Serial('/dev/ttyACM0',9600)

    #viewers need to register for one of two teams
    registered_users = {}

    numRed=0;
    numBlue=0
    #list of lists for commands. Red team then blue team. Forward, back, left, right
    commands_list=[[0,0,0,0],[0,0,0,0]]
    command_lookup={'f':0, 'b':1,'l':2,'r':3}
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

                # if user is not registered. All cases handle bug where "tmi" (name of twitch irc server) registers as player
                if not registered_users.has_key(username) and username!="tmi" and username!=NICK:
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

                        if command_lookup.has_key(message):
                            commands_list[registered_users.get(username)][command_lookup.get(message)]+=1
                            print commands_list
                            if registered_users.get(username)==0:
                                ser.write(struct.pack('>BB', mvmt_val.anarchy_val(commands_list,0),0))
                            else:
                                ser.write(struct.pack('>BB', 0, mvmt_val.anarchy_val(commands_list,1)))
                            print('team: '+str(registered_users.get(username)))
                            print('command: '+ str(mvmt_val.anarchy_val(commands_list,registered_users.get(username))))
                            commands_list=[[0,0,0,0],[0,0,0,0]]

def loop_b():
    ser = serial.Serial('/dev/ttyACM0',9600)
    while True:
        data = ser.readline()[:-2]
        if data:
            print(data)
Process(target = loop_a).start()
Process(target = loop_b).start()

                        #t_end = time.time() + 5
                    #    while time.time() < t_end:
