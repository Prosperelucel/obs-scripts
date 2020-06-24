#Scene sequence script

import sys
import logging
import os
import random
import time
from Sequence_SCENES_Config import *

os.chdir(sys.path[0])
sys.path.append('../')
logging.basicConfig(level=logging.ERROR)

#### CONFIG OBSWEBSOCKET ####
from obswebsocket import obsws, requests, events
ws = obsws(host, port, password)
ws.connect()

##############################

def gen_transition_rng(min_rng, max_rng):
    global transition_rng
    global transition_old_rng
    transition_rng_file = open(transition_txt, "r")
    transition_old_rng = transition_rng_file.readline().strip()
    transition_old_rng = int(transition_old_rng)
    transition_rng_file.close()
    transition_rng = random.randint(min_rng, max_rng)
    if transition_old_rng == transition_rng:
        gen_transition_rng(min_rng, max_rng)
    else:
        transition_rng_file = open(transition_txt, "w")
        transition_rng_file.write('{}'.format(transition_rng))
        transition_rng_file.close()
        return transition_rng

def gen_scene_rng(min_rng, max_rng):
    global scene_rng
    global scene_old_rng
    scene_rng_file = open(scene_txt, "r")
    scene_old_rng = scene_rng_file.readline().strip()
    scene_old_rng = int(scene_old_rng)
    scene_rng_file.close()
    scene_rng = random.randint(min_rng, max_rng)
    if scene_old_rng == scene_rng:
        gen_scene_rng(min_rng, max_rng)
    else:
        scene_rng_file = open(scene_txt, "w")
        scene_rng_file.write('{}'.format(scene_rng))
        scene_rng_file.close()
        return scene_rng


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


def get_scenes():
    global current_scene
    current_scene = ws.call(requests.GetCurrentScene()).getName()
    current_scene = str(current_scene)


def event_TransitionBegin(message):
    #print "|||||||||||||event_TransitionBegin"
    global event_fromScene
    global event_toScene
    global event_transition_isOn
    event_transition_isOn = True
    event_toScene = (message.getToScene())
    event_fromScene = (message.getFromScene())
    event_transition_duration = (message.getDuration())
    #print ("event_fromScene : ",event_fromScene)
    #print ("event_toScene : ",event_toScene)
    #print ("event_transition_duration : ",event_transition_duration)
    #print ("event_transition_isOn : ",event_transition_isOn)
    if event_toScene != next_scene:
        set_toggle(0)


def event_SwitchScenes(message):
    #print "|||||||||||||event_SwitchScenes"
    global event_SwitchScenes
    global event_transition_isOn
    event_SwitchScenes = (message.getSceneName())
    #print ("event_SwitchScenes : ", event_SwitchScenes)
    if event_SwitchScenes == event_toScene:
        event_transition_isOn = False
        #print ("event_transition_isOn : ", event_transition_isOn)


if __name__ == '__main__':
    ws.register(event_TransitionBegin, events.TransitionBegin)
    ws.register(event_SwitchScenes, events.SwitchScenes)

    check_toggle()
    if toggle_mode is True:
        #print "Toggle mode is ON"
        if toggle == 1:
            #print "Script is ON, STOP NOW"
            set_toggle(0)
            exit()
    else:
        if toggle == 1:
            #print "Script is ON, STOP NOW"
            exit()

#Get the default Transition
    current_transition_name = ws.call(requests.GetCurrentTransition()).getName()
    if current_transition_name != "Cut":
        current_transition_duration = ws.call(requests.GetCurrentTransition()).getDuration()

    #If transition_override is true we change the transition style
    if transition_override is True and transition_random is False and transition_sequence is False:
        ws.call(requests.SetCurrentTransition(transition_list[0]))  # Type
        if transition_list[0] != "Cut":
            ws.call(requests.SetTransitionDuration(transition_duration))  #Duration

#First launch, write 1 on toggle file
    set_toggle(1)

    scenes_numbers = len(scenes_list)
    transition_numbers = len(transition_list)
    next_transition = 0
    #print ("__STARTING SCRIPT, __REPEAT MODE :",repeat_mode,"__TOGGLE MODE :", toggle_mode)
    #print ("__Transition Override :", transition_override,"__Random", transition_random,"__Sequence", transition_sequence)
    #print ("__Scene List:", scenes_list)
    #print ("__Nombres de Scenes", scenes_numbers)
    #print ("__Transition List", transition_list)
    #print ("__Nombres de Transitions", transition_numbers)

    while toggle == 1:
        get_scenes()
        check_toggle()
        if toggle == 0:
            break

        for scenes in scenes_list:
            check_toggle()
            if toggle == 0:
                break

            if transition_override is True and transition_random is True and transition_sequence is False:
                gen_transition_rng(0, transition_numbers - 1)
                ws.call(requests.SetCurrentTransition(transition_list[transition_rng]))
                if transition_list[transition_rng] != "Cut":
                    ws.call(requests.SetTransitionDuration(transition_duration))  #Duration
            elif transition_override is True and transition_sequence is True and transition_random is False:
                    next_transition += 1
                    #print next_transition
                    #print ('current transition : ', transition_list[next_transition])
                    ws.call(requests.SetCurrentTransition(transition_list[next_transition]))
                    if transition_list[next_transition] != "Cut":
                        ws.call(requests.SetTransitionDuration(transition_duration))  #Duration
                    if next_transition >= (transition_numbers - 1):
                        next_transition = 0

            if scenes_random is True:
                gen_scene_rng(0, scenes_numbers - 1)
                next_scene = scenes_list[scene_rng]
                if next_scene == current_scene:
                    gen_scene_rng(0, scenes_numbers - 1)
                    next_scene = scenes_list[scene_rng]
                ws.call(requests.SetCurrentScene(next_scene))
            else:
                next_scene = scenes
                ws.call(requests.SetCurrentScene(next_scene))

            #print ("|||||||||||||next_scene", next_scene)
            #print "|||||||||||||Pause"
            time.sleep(transition_tempo)
            #print "|||||||||||||End Pause"

            if next_scene != current_scene:
               while event_transition_isOn is True:
                   time.sleep(0.1)
                   #print "Transition ON"
               else:
                   #print "Transition OFF, PASS"
                   pass

            get_scenes()
            if next_scene != current_scene and scenes_random is False:
                #print "Manual scene switch detected, stop now"
                set_toggle(0)
                break
            elif scenes_random is True:
                if next_scene != current_scene:
                    #print "Manual scene switch detected, stop now"
                    set_toggle(0)
                    break

        if repeat_mode is False:
            #print "repeat mode false"
            break

    #print "while loop break"

    #Bring back the default transition
    ws.call(requests.SetCurrentTransition(current_transition_name))  #Type
    if current_transition_name != "Cut":
        ws.call(requests.SetTransitionDuration(current_transition_duration))  #Duration
    time.sleep(0.5)
    if scene_end_mode == True:
        ws.call(requests.SetCurrentScene(scene_end))

    set_toggle(0)
    exit()

