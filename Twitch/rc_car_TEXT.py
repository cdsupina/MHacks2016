#@author: Varoon
#This script is meant to listen to the twitch stream from hot_glue_from_purdue, interact with the 
#players in the stream, and send the "consensus" of the players to the console. Mainly for testing
# This will also assign and maintain teams.  
import socket
import time
import re
import random
import mvmt_val

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
    if time.time()-current_time>2:     
        a=mvmt_val.get_mvmt_val(commands,0)
        b=mvmt_val.get_mvmt_val(commands,1)
        current_time=time.time()
        print [a,b]
        #commands=[[0,0,0,0],[0,0,0,0]]      #resets commands list
        
    else:
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
                    try:
                        if command_lookup.has_key(message):
                            commands[registered_users.get(username)][command_lookup.get(message,0)]+=1
          
                    except:
                        s.send('PRIVMSG %s :%s\r\n' % (CHAN, '{} has an invalid entry. Remember, only enter f,b,l,or r.\n'.format(username).encode('utf-8')))
