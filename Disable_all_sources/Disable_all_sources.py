#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Prospere Dirty Script

scene = "Scene_name"
exception_list = ["not_this_source", "not_this_one","not_me"]
host = "localhost"
port = 4444
password = "password"

import sys
import logging
import os
from threading import Thread

os.chdir(sys.path[0])
sys.path.append('../')
#logging.basicConfig(level=logging.DEBUG)
from obswebsocket import obsws, requests

ws = obsws(host, port, password)


def sendpacket(packet):
    ws.send(packet)

def getSourcesList(list):
    result = []
    for element in list:
        if (current_scene in element["name"]):
            for value in element["sources"]:
                result.append(value["name"])
    return result

def getSourcesListWhenRender(list):
    result = []
    for element in list:
        if (current_scene in element["name"]):
            for value in element["sources"]:
                if (value[u'render']):
                    result.append(value[u'name'])
    return result


ws.connect()

current_scene = scene
get_scenes_list = ws.call(requests.GetSceneList())
scenes_list = get_scenes_list.datain
sources_list = getSourcesList(scenes_list[u'scenes'])
#sources_render = getSourcesListWhenRender(scenes_list[u'scenes'])

for exception in exception_list:
    if exception in sources_list:
        sources_list.remove(exception)

packets = []
#Préparation des packets
for sources in sources_list:
    packet = {"request-type": "SetSceneItemProperties", "item": sources, "visible": False, "scene-name": current_scene}
    packets += [packet]

#Lancement des Threads
for packet in packets:
    t = Thread(target=sendpacket, args=(packet,))
    t.start()
