#Prospere Dirty Script
#Randomly generate text regarding the words in the lists

#################################################################################################################
host = "localhost"
port = 4444
password = "password"
#################################################################################################################
source_txt = "my_text_source"
list_txt1 = "List1.txt"
list_txt2 = "List2.txt"
list_txt3 = "List3.txt"
list_txt4 = "List4.txt"
#################################################################################################################

import sys
import logging
import os
import random
from random import randint
import time
from threading import Thread

#set dir to script folder
os.chdir(sys.path[0])
sys.path.append('../')
logging.basicConfig(level=logging.ERROR)

from obswebsocket import obsws, requests, events

ws = obsws(host, port, password)
ws.connect()
#Send data to OBS
def sendpacket(packet):
    ws.send(packet)

if __name__ == '__main__':
    with open(list_txt1) as f:
        lines = f.readlines()
        selection_1 = (random.choice(lines))

    with open(list_txt2) as f:
        lines = f.readlines()
        selection_2 = (random.choice(lines))

    with open(list_txt3) as f:
        lines = f.readlines()
        selection_3 = (random.choice(lines))

    with open(list_txt4) as f:
        lines = f.readlines()
        selection_4 = (random.choice(lines))

    txt_result = (selection_1.rstrip() + " " +  selection_2.rstrip() + " " + selection_3.rstrip()+ " " + selection_4.rstrip())

    ws.call(requests.SetTextGDIPlusProperties(source=source_txt, text=txt_result))
    ws.disconnect()
    exit()
