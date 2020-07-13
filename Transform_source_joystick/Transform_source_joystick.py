#Move source with Xbox One controller

#### CONFIG ####
host = "localhost"
port = 4444
password = "password"
#### OBS CONFIG ####
scene = "Scene_name"
source_name = "Source_Name"

import sys
import logging
import os
import random
import time
import threading
from threading import Thread
from obswebsocket import obsws, requests, events
import pygame, sys,os
from pygame.locals import *

os.chdir(sys.path[0])
sys.path.append('../')
#logging.basicConfig(level=logging.DEBUG)



def sendthread(packet):
    #print (threading.activeCount())
    #if threading.activeCount() < 12:
    t = Thread(target=sendpacket, args=(packet,))
    t.start()


def callthread(packet):
    t = Thread(target=sendcall, args=(packet,))
    t.start()
    t.join()

def sendpacket(packet):
    ws.send(packet)

def sendcall(packet):
    ws.call(packet)

def join(t):
    if not t.isAlive():
        t.join()

ws = obsws(host, port, password)
ws.connect()

incremental_x = 20
incremental_y = 20
incremental_z = 0.05
inc_rotation = 2

###get value from the source
item_state = ws.call(requests.GetSceneItemProperties(scene_name=scene, item=source_name))
filter_state = ws.call(requests.GetSourceFilters(sourceName=source_name))
filter_list = filter_state.datain
#print filter_list, "filter_list"
filter_type = filter_list[u'filters']
if filter_type:
    #print filter_type,"filter_type"
    filter_name = filter_type[0]
    #print filter_name, "filter_name"
    filter_name = filter_name[u'name']
    #print filter_name, "filter_name"
    filter_visibility = filter_type[0]
    #print filter_visibility, "filter_visibility"
    filter_visibility = filter_visibility[u'enabled']
    #print filter_visibility, "filter_visibility"
    filteronsource = True

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
reset_visibility = source_visibility

#print ("ITEM_STATE----------------")
#print (item_state)
#print ("ITEM_LIST-----------------")
#print (item_list)
#print ("OLD_POSITION-----------------")
#print (old_position)
#print (old_pos_x)
#print (old_pos_y)
#print ("OLD_SCALE-----------------")
#print (old_scale)
#print (old_scale_x)
#print (old_scale_y)
#print ("ROTATION-----------------")
#print (old_rotation)
#print ("OLD_BOUNDS-----------------")
#print (old_bounds)
#print (old_bounds_x)
#print (old_bounds_y)

droite = False
gauche = False
haut = False
bas = False
zoom_in = False
zoom_out = False
rotation_down = False
rotation_up = False
timer_sleep = 0
command = False
command_gamepad = False
command_filter = False
command_count = 0
invert_x = False
invert_y = False
command_reset = False
packets = []
threads = []
pygame.init()
while True:

    if not pygame.event.get():
        if command_gamepad:
            command = True
        else:
            command = False

    time.sleep(0.035)

    if pygame.event.get():
        command = True

    if command:
        command_gamepad = False
        command = False
        packet01 = {"request-type": "SetSceneItemProperties", "scene-name": scene, "item": source_name,"position": {"x": old_pos_x,"y": old_pos_y},"scale": {"x": old_scale_x,"y": old_scale_y},"rotation": old_rotation,"visible": source_visibility}
        sendthread(packet01)
        if command_reset:
            time.sleep(2)
            ws.disconnect()
            exit()

    if droite:
        old_pos_x += incremental_x
    if gauche:
        old_pos_x -= incremental_x
    if haut:
        old_pos_y -= incremental_y
    if bas:
        old_pos_y += incremental_y

    if zoom_in:
        if invert_x:
            old_scale_x -= incremental_z
            old_scale_y += incremental_z

        if invert_y:
            old_scale_x += incremental_z
            old_scale_y -= incremental_z

        if invert_y and invert_x:
            old_scale_x -= incremental_z
            old_scale_y -= incremental_z

        if not invert_y and not invert_x:
            old_scale_x += incremental_z
            old_scale_y += incremental_z

    if zoom_out:
        if invert_x:
            old_scale_x += incremental_z
            old_scale_y -= incremental_z

        if invert_y:
            old_scale_x -= incremental_z
            old_scale_y += incremental_z

        if invert_y and invert_x:
            old_scale_x += incremental_z
            old_scale_y += incremental_z

        if not invert_y and not invert_x:
            old_scale_x -= incremental_z
            old_scale_y -= incremental_z

    if rotation_up:
        old_rotation += inc_rotation
    if rotation_down:
        old_rotation -= inc_rotation

    joystick_count = pygame.joystick.get_count()
    if joystick_count > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        name = joystick.get_name()
        axes = joystick.get_numaxes()
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        axis_zoom_in = joystick.get_axis(5)
        axis_zoom_out = joystick.get_axis(2)
        axis_rotation = joystick.get_axis(3)
        button_A = joystick.get_button(0)
        button_B = joystick.get_button(1)
        button_X = joystick.get_button(2)
        button_Y = joystick.get_button(3)
        buttonLT = joystick.get_button(4)
        buttonRT = joystick.get_button(5)
        button_select = joystick.get_button(6)
        button_start = joystick.get_button(7)
        button_LeftStick = joystick.get_button(8)
        button_RightStick = joystick.get_button(9)

        #print button_A,"A"
        #print button_B,"B"
        #print button_X,"X"
        #print button_Y,"Y"
        #print buttonLT,"LT"
        #print buttonRT,"RT"
        #print button_select,"Select"
        #print button_start,"Start"
        #print button_LeftStick,"LeftStick"
        #print button_RightStick,"RightStick"

        dpad = joystick.get_hat(0)
        dpad_x = dpad[0]
        dpad_y = dpad[1]

        if axis_rotation > 0.3:
            rotation_up = True
            rotation_down = False
            command_gamepad = True
        if axis_rotation < -0.3:
            rotation_up = False
            rotation_down = True
            command_gamepad = True
        if axis_rotation > -0.3 and axis_rotation < 0.3:
            rotation_down = False
            rotation_up = False

        if axis_zoom_in > -0.8:
            zoom_in = True
            zoom_out = False
            command_gamepad = True
        if axis_zoom_out > -0.8:
            zoom_in = False
            zoom_out = True
            command_gamepad = True
        if axis_zoom_out < -0.8 and axis_zoom_in < -0.8 :
            zoom_in = False
            zoom_out = False

        if axis_x > 0.3 or dpad_x > 0: #Right
            droite = True
            gauche = False
            command_gamepad = True

        if axis_x < -0.3 or dpad_x < 0: #Left
            droite = False
            gauche = True
            command_gamepad = True

        if axis_y < -0.3 or dpad_y > 0: #Top
            haut = True
            bas = False
            command_gamepad = True

        if axis_y > 0.3 or dpad_y < 0: #Bot
            haut = False
            bas = True
            command_gamepad = True

        if axis_y < 0.3 and axis_y > -0.3 and axis_x < 0.3 and axis_x > -0.3 and dpad_x < 0.1 and dpad_x > -0.1 and dpad_y < 0.1 and dpad_y > -0.1: #center
            haut = False
            bas = False
            droite = False
            gauche = False

        #Reset Position
        if button_B == 1:
            command_gamepad = True
            old_pos_x = reset_pos_x
            old_pos_y = reset_pos_y

        #Reset Rotation
        if button_X == 1:
            command_gamepad = True
            old_rotation = reset_rotation

        #Reset Scale
        if button_Y == 1:
            command_gamepad = True
            old_scale_x = reset_scale_x
            old_scale_y = reset_scale_y

        #ToggleVisibility
        if button_A == 1:
            command_gamepad = True
            if source_visibility:
                source_visibility = False
            else:
                source_visibility = True


        #Invert X scale
        if buttonLT == 1:
            time.sleep(0.1)
            if not invert_x:
                invert_x = True
            else:
                invert_x = False
            command_gamepad = True
            old_scale_x = -old_scale_x

        #Invert Y scale
        if buttonRT == 1:
            time.sleep(0.1)
            if not invert_y:
                invert_y = True
            else:
                invert_y = False
            command_gamepad = True
            old_scale_y = -old_scale_y

        #Toggle Filter
        if button_start == 1:
            if filteronsource:
                if filter_visibility:
                    filter_visibility = False
                    callthread(requests.SetSourceFilterVisibility(sourceName=source_name, filterName=filter_name,filterEnabled=filter_visibility))
                else:
                    filter_visibility = True
                    callthread(requests.SetSourceFilterVisibility(sourceName=source_name, filterName=filter_name,filterEnabled=filter_visibility))

        #Exit Script / Reset Source
        if button_select == 1:
            old_pos_x = reset_pos_x
            old_pos_y = reset_pos_y
            old_scale_y = reset_scale_y
            old_scale_x = reset_scale_x
            old_rotation = reset_rotation
            command_reset = True

    if joystick_count == 0:
        ws.disconnect()
        exit()

    #clock.tick(120)


