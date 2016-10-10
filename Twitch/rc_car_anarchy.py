#@author: Varoon
#This script is meant to listen to the twitch stream from hot_glue_from_purdue, interact with the
#players in the stream, and send the "consensus" of the players to the console. Mainly for testing
# This will also assign and maintain teams.
import socket
import re
import random
import mvmt_val
import serial
import struct
from multiprocessing import Process
import time
#gives the introductory messages to the users.

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


def pick_other_team(x):
    if int(x)==1:
        return 0
    return 1
def loop_a():

    #viewers need to register for one of two teams
    registered_users = {}

    numRed=0;
    numBlue=0
    #list of lists for commands. Red team then blue team. Forward, back, left, right
    commands_list=[[0,0,0,0],[0,0,0,0]]
    command_lookup={'f':0, 'b':1,'l':2,'r':3}
    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")



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
            #WIN CONDITION!!
                message=''

                if registered_users.has_key(username):
                    message = CHAT_MSG.sub("",line).rstrip()
                    print 'message: '+message

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


#if data is 0, red team's post is knocked over and blue team wins. Vice versa. Send message to twitch.
def loop_b():

    while True:

        data = ser.readline()[:-2]
        if data:
            x=pick_other_team(data)
            s.send('PRIVMSG %s :%s\r\n' % (CHAN, 'The {} team won! Congratulations! Please give us time to reset.'.format(teams.get(x)).encode('utf-8')))
            print 'TEAM WON IS TRUE!!!'
            return

#global variable

CHAN = "#twitchplaysbattlebots"
teams={0:'Red',1:'Blue'}
HOST = "irc.twitch.tv"
PORT = 6667
NICK = "twitchplaysbattlebots"
PASS = "oauth:0dyincbnyg1swo4y4eirxn6iczixdo"

s = socket.socket()
s.connect((HOST,PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

for i in range(1,11):
    string = '/dev/ttyACM{}'.format(i)
    try:
        ser=serial.Serial(string,9600)
        break
    except Exception as e:
        continue
    print 'Could not find the serial port'
print ser.name
introduction_messages()
Process(target = loop_a).start()
Process(target = loop_b).start()
