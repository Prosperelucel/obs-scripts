#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Prospere Dirty Script
########################################################################################
#######################################CONFIG BLOCK#####################################
scene = "Scene_name"
sources_list = ["01", "02", "03", "04", "05","06","07","08"]
transition_tempo = 0.2
random_mode = False #False : Sequence mode / True : Random Mode

repeat_mode = True #(Sequence mode only) False : Play sequence one time / True : Loop Mode for sequence
clean_sources_at_start = True #Disable all sources in list at start

host = "localhost"
port = 4444
password = "password"

toggle_txt = "Sequence_SOURCES_Toggle.txt"
rng_txt = "Sequence_SOURCES_RNG.txt"
########################################################################################
########################################################################################


import sys
import logging
import os
import random
import time
from threading import Thread

os.chdir(sys.path[0])
sys.path.append('../')
#logging.basicConfig(level=logging.ERROR)
from obswebsocket import obsws, requests, events
ws = obsws(host, port, password)
ws.connect()

def sendpacket(packet):
    ws.send(packet)

def threadpacket(packet):
    t = Thread(target=sendpacket, args=(packet,))
    t.start()

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

#Generate RNG
def gen_rng(min_rng,max_rng):
    global rng
    global old_rng
    rng_file = open(rng_txt, "r")
    old_rng = rng_file.readline().strip()
    old_rng = int(old_rng)
    rng_file.close()
    rng = random.randint(min_rng, max_rng)
    if old_rng == rng:
        gen_rng(min_rng, max_rng)
    else:
        text_file = open(rng_txt, "w")
        text_file.write('{}'.format(rng))
        text_file.close()
        return rng

if __name__ == '__main__':
    check_toggle()
    if toggle == 1:
        set_toggle(0)
    else:
        set_toggle(1)

    sources_current = 0

    if clean_sources_at_start is True:
        for sources in sources_list:
            packet = {"request-type": "SetSceneItemProperties", "item": sources,
                      "visible": False,
                      "scene-name": scene}
            threadpacket(packet)

    while toggle == 1:

        #How many sources
        sources_numbers = len(sources_list)
        if random_mode:
            gen_rng(0, sources_numbers - 1)
            # Packet 01 : Disable source with OLD_RNG
            packet01 = {"request-type": "SetSceneItemProperties", "item": sources_list[old_rng], "visible": False,
                        "scene-name": scene}
            # Packet 02 : Activate source with New RNG
            packet02 = {"request-type": "SetSceneItemProperties", "item": sources_list[rng], "visible": True,
                        "scene-name": scene}
            packets = [packet01, packet02]
            for packet in packets:
                threadpacket(packet)
        else:
            #Sequence mode repeat
            if sources_current == sources_numbers and repeat_mode is True:
                sources_current = 0
            elif sources_current == sources_numbers and repeat_mode is False:
                packet04 = {"request-type": "SetSceneItemProperties", "item": sources_list[sources_current - 1],
                            "visible": False, "scene-name": scene}
                threadpacket(packet04)
                break

            #Disable last source
            packet01 = {"request-type": "SetSceneItemProperties", "item": sources_list[sources_current - 1],
                        "visible": False,
                        "scene-name": scene}
            #Activate next source
            packet02 = {"request-type": "SetSceneItemProperties", "item": sources_list[sources_current],
                        "visible": True,
                        "scene-name": scene}

            packets = [packet01, packet02]
            for packet in packets:
                threadpacket(packet)

            sources_current += 1



        #tempo
        time.sleep(transition_tempo)
        check_toggle()

    #Clean sources before exit
    for source in sources_list:
            packet03 = {"request-type": "SetSceneItemProperties", "item": source, "visible": False, "scene-name": scene}
            threadpacket(packet03)

    set_toggle(0)
    time.sleep(1)
    ws.disconnect()
    exit()
