#ShakeSource
import sys
import logging
import os
import random
import time
import threading
from threading import Thread
from obswebsocket import obsws, requests, events

#### CONFIG ####
host = "localhost"
port = 4444
password = "password"
#### OBS CONFIG ####
scene = "Scene_name"
source_name = "Source_Name"
random_position = 10
random_rotation = 5
toggle_txt = "Shake_Source_Toggle.txt"
timer = 0.05


os.chdir(sys.path[0])
sys.path.append('../')
#logging.basicConfig(level=logging.DEBUG)

def sendthread(packet):
    t = Thread(target=sendpacket, args=(packet,))
    t.start()

def callthread(packet):
    t = Thread(target=sendcall, args=(packet,))
    t.start()

def sendpacket(packet):
    ws.send(packet)

def sendcall(packet):
    ws.call(packet)

def check_toggle():
    global toggle
    toggle_file = open(toggle_txt, "r")
    toggle = toggle_file.readline().strip()
    toggle = int(toggle)
    toggle_file.close()
    return toggle

def set_toggle(value):
    global toggle
    toggle = value
    toggle_file = open(toggle_txt, "w")
    toggle_file.write('{}'.format(toggle))
    toggle_file.close()
    return toggle

ws = obsws(host, port, password)
ws.connect()

###get value from the source#############################################################
item_state = ws.call(requests.GetSceneItemProperties(scene_name=scene, item=source_name))
item_list = item_state.datain
old_position = item_list[u'position']
old_pos_x = old_position['x']
old_pos_y = old_position['y']
old_scale = item_list[u'scale']
old_scale_x = old_scale['x']
old_scale_y = old_scale['y']
old_rotation = item_list[u'rotation']
old_bounds = item_list[u'bounds']
old_bounds_x = old_bounds['x']
old_bounds_y = old_bounds['y']
source_visibility = item_list[u'visible']
########################################################################################

old_rotation = round(old_rotation, 2)
old_scale_x = round(old_scale_x, 2)
old_scale_y = round(old_scale_y, 2)
old_bounds_x = round(old_bounds_x, 2)
old_bounds_y = round(old_bounds_y, 2)

reset_pos_x = old_pos_x
reset_pos_y = old_pos_y
reset_scale_x = old_scale_x
reset_scale_y = old_scale_y
reset_rotation = old_rotation
reset_bounds_x = old_bounds_x
reset_bounds_y = old_bounds_y

locked = False
visible = True
pos_x = old_pos_x
pos_y = old_pos_y
scale_x = old_scale_x
scale_y = old_scale_y
rotation = old_rotation

crop_top = 0
crop_bot = 0
crop_left = 0
crop_right = 0
bounds = "OBS_BOUNDS_NONE" ###"OBS_BOUNDS_STRETCH", "OBS_BOUNDS_SCALE_INNER", "OBS_BOUNDS_SCALE_OUTER", "OBS_BOUNDS_SCALE_TO_WIDTH", "OBS_BOUNDS_SCALE_TO_HEIGHT", "OBS_BOUNDS_MAX_ONLY" or "OBS_BOUNDS_NONE".
bounds_x = 1920
bounds_y = 1080
b_alignment = 0
p_alignment = 0

check_toggle()

if toggle == 1:
    set_toggle(0)
    exit()
set_toggle(1)

while True:
    check_toggle()
    if toggle == 0:
        exit()
    pos_x = old_pos_x + random.randint(-random_position,random_position)
    pos_y = old_pos_y + random.randint(-random_position,random_position)
    rotation = old_rotation + random.randint(-random_rotation,random_rotation)

    time.sleep(timer)

    sendthread({"request-type": "SetSceneItemProperties",
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
