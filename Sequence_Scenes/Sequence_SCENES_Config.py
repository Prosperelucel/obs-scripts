########################################################################################
#######################################CONFIG BLOCK#####################################

scenes_list = ["scene_01", "scene_02", "scene_03", "scene_04","scene_05"]
transition_list = ["Slide", "Fade", "Luma Wipe", "Fade to Color Black", "Fade to Color"] #Transition Random

scene_end = "Webcam" #Ending scene
scene_end_mode = True #True = When script ending go back to the scene_end

########################################################################################
########################################################################################

repeat_mode = False #True = Infinite mode / False = Play sequence one time
toggle_mode = True #True = Enable script On/Off / False = Disable script On/Off (need use the togglescript.py to stop)
scenes_random = False #True = Scenes will be played randomly / False = Scenes will be played in order (left to right)

########################################################################################
########################################################################################
transition_override = True #True = Override the OBS-Studio current transition and use the transition_list list / False = Use OBS-Sutio current transition for all transition between scenes

########################################################################################
########################################################################################

transition_random = False #True = Randomly select transition from the list / False = First item in the list will be used as main transition
transition_sequence = False #True = Transition will be chosen in the order of the list / False = Disable sequence read
#if random and sequence are false Only the FIRST item in the transition list will be used

########################################################################################
########################################################################################

transition_duration = 500 #Duration of transition in ms
transition_tempo = 1 #Duration of the sleep timer in s

########################################################################################
########################################################################################

toggle_txt = "Sequence_SCENES_Toggle.txt"
transition_txt = "Sequence_SCENES_Transition_RNG.txt"
scene_txt = "Sequence_SCENES_Scene_RNG.txt"

########################################################################################
########################################################################################
