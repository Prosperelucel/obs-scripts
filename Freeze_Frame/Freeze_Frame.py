#Freeze Frame Effect
#Screenshot the current scene and transition to the "freezeframe" scene

import sys
import logging
import os
import time
from Freeze_Frame_Config import *
start = time.time()
os.chdir(sys.path[0])
print ("os.getcwd", os.getcwd())
sys.path.append('../')
logging.basicConfig(level=logging.ERROR)
from obswebsocket import obsws, requests, events
ws = obsws(host, port, password)
ws.connect()
def sendpacket(packet):
    ws.send(packet)
try:
    scene_to_screenshot = ws.call(requests.GetCurrentScene()).getName()
    scene_to_screenshot = str(scene_to_screenshot)

    if freeze_scene != scene_to_screenshot:
        packet01 = {"request-type": "TakeSourceScreenshot", "sourceName": scene_to_screenshot, "width": 1280, "height": 720, "saveToFilePath": file_path}
        packet02 = {"request-type": "SetCurrentScene", "scene-name": freeze_scene}
        sendpacket(packet01)
        sendpacket(packet02)
    else:
        ws.disconnect()
except:
    ws.disconnect()
#packet = {"request-type": "TakeSourceScreenshot", "sourceName": scene_to_screenshot, "PictureFormat": "Jpg", "saveToFilePath": "J:\_Stream\Prospere\_Tools\OBSCommand\Replay\Replay.png"}
