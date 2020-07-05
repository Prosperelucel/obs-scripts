#SetItemProperties
#### WS CONFIG####
host = "localhost"
port = 4444
password = "password"

#### SOURCE CONFIG ####
scene = "Scene_name" #optional
source_name = "Source_Name"
locked = False
visible = True
pos_x = 960
pos_y = 540
scale_x = 0.5
scale_y = 0.5
rotation = 90
crop_top = 0
crop_bot = 0
crop_left = 0
crop_right = 0
bounds = "OBS_BOUNDS_NONE" ###"OBS_BOUNDS_STRETCH", "OBS_BOUNDS_SCALE_INNER", "OBS_BOUNDS_SCALE_OUTER", "OBS_BOUNDS_SCALE_TO_WIDTH", "OBS_BOUNDS_SCALE_TO_HEIGHT", "OBS_BOUNDS_MAX_ONLY" or "OBS_BOUNDS_NONE".
bounds_x = 4
bounds_y = 4
#bounds alignment
b_alignment = 0
#position alignment
p_alignment = 0
###ALIGNMENT TYPE :
### 0 = Center
### 1 = Center left
### 2 = Center Right
### 3 =
### 4 = Top Center
### 5 = Top Left
### 6 = Top Right
### 7 =
### 8 = Bottom Center
### 9 = Bottom Left
### 10 = Bottom Right
### 11 =
#### END SOURCE CONFIG ####

import sys
import logging
import os
import random
import time
from threading import Thread
from obswebsocket import obsws, requests, events

os.chdir(sys.path[0])
sys.path.append('../')
logging.basicConfig(level=logging.DEBUG)

def sendpacket(packet):
    ws.send(packet)

ws = obsws(host, port, password)
ws.connect()

try:
    sendpacket({"request-type": "SetSceneItemProperties",
                "scene-name": scene,
                "item": source_name,
                "position": {"x": pos_x,
                             "y": pos_y,
                             "alignment": p_alignment},
                "rotation": rotation,
                "scale": {"x": scale_x,
                          "y": scale_y},
                "bounds": {"alignment": b_alignment,
                           "type": bounds,
                           "x": bounds_x,
                           "y": bounds_y},
                "locked": locked,
                "crop": {"bottom": crop_bot,
                         "left": crop_left,
                         "right": crop_right,
                         "top": crop_top},
                "visible": visible})


except KeyboardInterrupt:
    pass

ws.disconnect()
