#Move source with Xbox One controller

#### CONFIG ####
host = "localhost"
port = 4444
password = "password"
#### OBS CONFIG ####
scene = "Scene A"
source_name = "Webcam"

import sys
import logging
import os
import random
import time
from threading import Thread
from obswebsocket import obsws, requests, events
import pygame, sys,os
from pygame.locals import *

os.chdir(sys.path[0])
sys.path.append('../')
logging.basicConfig(level=logging.ERROR)

def sendpacket(packet):
    ws.send(packet)

def sendcall(packet):
    ws.call(packet)

ws = obsws(host, port, password)
ws.connect()

incremental_x = 5
incremental_y = 5
incremental_z = 0.01
inc_rotation = 1

###get value from the source
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

reset_pos_x = old_pos_x
reset_pos_y = old_pos_y
reset_scale_x = old_scale_x
reset_scale_y = old_scale_y
reset_rotation = old_rotation
reset_bounds_x = old_bounds_x
reset_bounds_y = old_bounds_y

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

pygame.init()

while True:
    time.sleep(0.025)

    if not pygame.event.get():
        if command_gamepad:
            command = True
        else:
            command = False

    if pygame.event.get():
        command = True

    if command:
        command_gamepad = False
        packet01 = {"request-type": "SetSceneItemPosition", "scene-name": scene, "item": source_name, "x": old_pos_x, "y": old_pos_y}
        packet02 = {"request-type": "SetSceneItemTransform", "scene-name": scene, "item": source_name, "x-scale": old_scale_x, "y-scale": old_scale_y, "rotation": old_rotation}
        packets = [packet01, packet02]
        for packet in packets:
            t = Thread(target=sendpacket, args=(packet,))
            t.start()

    if droite:
        old_pos_x += incremental_x
    if gauche:
        old_pos_x -= incremental_x
    if haut:
        old_pos_y -= incremental_y
    if bas:
        old_pos_y += incremental_y
    if zoom_in:
        old_scale_x += incremental_z
        old_scale_y += incremental_z
    if zoom_out:
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
        button1 = joystick.get_button(1)
        button2 = joystick.get_button(2)
        button3 = joystick.get_button(3)
        button_select = joystick.get_button(6)
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

        if button1 == 1:
            command_gamepad = True
            old_pos_x = reset_pos_x
            old_pos_y = reset_pos_y
            old_scale_x = reset_scale_x
            old_scale_y = reset_scale_y
            old_rotation = reset_rotation


        if button2 == 1:
            command_gamepad = True
            old_rotation = reset_rotation

        if button3 == 1:
            if source_visibility:
                #ws.call(requests.SetSceneItemRender(scene_name=scene, source=source_name, render=False))
                #sendpacket({"request-type": "SetSceneItemRender", "scene-name": scene, "source": source_name, "render":False})

                packet = {"request-type": "SetSceneItemRender", "scene-name": scene, "source": source_name, "render":False}
                t = Thread(target=sendpacket, args=(packet,))
                t.start()
                source_visibility = False
                t.join(1)
            else:
                #ws.call(requests.SetSceneItemRender(scene_name=scene, source=source_name, render=True))
                #sendpacket({"request-type": "SetSceneItemRender", "scene-name": scene, "source": source_name, "render": True})

                packet = {"request-type": "SetSceneItemRender", "scene-name": scene, "source": source_name, "render":True}
                t = Thread(target=sendpacket, args=(packet,))
                t.start()
                source_visibility = True
                t.join(1)

        if button_select == 1:
            old_pos_x = reset_pos_x
            old_pos_y = reset_pos_y
            old_scale_x = reset_scale_x
            old_scale_y = reset_scale_y
            old_rotation = reset_rotation
            ws.call(requests.SetSceneItemPosition(scene_name=scene, item=source_name, x=old_pos_x, y=old_pos_y))
            ws.call(requests.SetSceneItemTransform(scene_name=scene, item=source_name, x_scale=old_scale_x,y_scale=old_scale_y, rotation=old_rotation))
            exit()

    if joystick_count == 0:
        exit()
        ws.disconnect()

    #clock.tick(120)


