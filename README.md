# Prospere's dirty scripts for OBS
Collection of dirty python script for Open Broadcast software.
I'm not a professional developper, I do this on my free time for friends, I'm just a French guy who love "la bidouille" :)

Important : Currently most of the script will NOT work in "Studio mode".


### Requirement :
- Windows 10
- [OBS Studio](https://obsproject.com/)
- [Python27](https://www.python.org/ftp/python/2.7/python-2.7.amd64.msi)
- [obs-websocket](https://github.com/Palakis/obs-websocket) from [@LePalakis](https://twitter.com/LePalakis)
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) from Guillaume Genty a.k.a Elektordi


### Installation and dependencies : 
- Install Python27
- Open command prompt or a terminal (windows key + R, type "cmd" and enter)
- Go to your Python27 folder in the command prompt (cd c:\Python27)

All the script requiere the python library obs-websocket-py
- type in the cmd

```
python.exe -m pip install obs-websocket-py
```

- Install [obs-websocket](https://github.com/Palakis/obs-websocket) for Obs Studio
- Edit the websocket config like this and change your password 

- ![](https://i.imgur.com/gOvPhwx.jpg)



### Python27 + Streamdeck Usage :
- Execute the script with Pythonw.exe for silent execution (no console showing)
- On Windows explorer, right click on the python script, select "Open With" and "Choose another app"
- Tick the box for permanently use the same app, go "find on the computer" in the bottom list and finaly select pythonw.exe in the c:\Python27 folder
- Now simply add the main script to your Streamdeck using the app shortcut

- Or if you don't want to change the windows default execution for python file you can add this line to your Streamdeck app launch button : 

```
"C:\Python27\pythonw.exe  C:\Script\Yourscript.py"
```



---

## 01 - Sequence Scenes
Trigger a sequence of scenes regarding a list and a config file
#### Configuration:
Edit Sequence_SCENES_Config.py and replace with your obs-websocket password
```
host = "localhost"
port = 4444
password = "password"
```
edit the scenes_list and transition_list with your own scene/transition
```
scenes_list = ["scene_01", "scene_02", "scene_03", "scene_04","scene_05"]
transition_list = ["Slide", "Fade", "Luma Wipe", "Fade to Color Black", "Fade to Color"] #Transition Random
```

To start the script launch Scene_Sequence.py with a Streamdeck or with the Windows explorer
#### Example:
https://twitter.com/i/status/1153650170564894721

---

## 02 - Freeze Frame
Capture a picture of the current active scene and save it into a specific folder/file
Then switch to a "freeze frame" scene

#### Script Configuration:
Edit Freeze_Frame_Config.py and replace with your obs-websocket password
```
host = "localhost"
port = 4444
password = "password"
```
edit the freeze_scene and file_path with your own
```
freeze_scene = "Freeze_Frame"
file_path = "c:\_Stream\Replay.bmp"
```
#### OBS Studio Configuration:
- In Windows explorer, go to your file_path and create and empty image, name it Replay.bmp
- In Obs Create a new scene with the same name (ex: Freeze_Frame) and import the empty image.
- I suggest to create a new transition for this effect like "Fade to White"
- Right click on the "Freeze_Frame" scene and set a "transition overide" to Fade to White

To start the script launch Freeze_Frame.py with a Streamdeck or with the Windows explorer

#### Example:
https://twitter.com/ProspereLucel/status/1153655792861626369

---

## 03 - Random Text Generator
Change the content of a Text source (GDI+) randomly regarding multiple text list.

#### Script Configuration:
Edit Random_Txt.py and replace with your obs-websocket password
```
host = "localhost"
port = 4444
password = "password"
```
edit the source_txt with yours
```
source_txt = "my_text_source"
```
edit the content of the 4 texts lists with your "funny words" lol xD
If you want to use less list, leave at least two empty lines inside the .txt file otherwise the script will not work

#### OBS Studio Configuration:
- Create a text source with the source_txt name (ex : "my_text_source")
- Right click and transform your source, Edit transform, set "Positional Alignment" to "Center"
- Edit the text "Properties" and choose your text style and Alignment. 

To start the script launch Random_Txt.py with a Streamdeck or with the Windows explorer

#### Example:
![](https://i.imgur.com/qfS9irb.jpg)

---

## 04 - Transform source with Gamepad/Joystick

#### Script Configuration:
Edit the script and replace with your obs-websocket password
```
host = "localhost"
port = 4444
password = "password"
```
edit the "scene" and the source you want to move with yours
```
scene = "Scene A"
source_name = "source_name"
```
#### OBS Studio Configuration:
- Right click on the source and setup transformation settings to "No Bounds" and "Center alignement"

#### Python requirement:
- [pygame](https://www.pygame.org/)
```
Python.exe -m pip install pygame==2.0.0.dev10
```
To start the script launch Transform_source_joystick.py with a Streamdeck or with the Windows explorer

#### Xbox one controller Layout:
- Left Stick / Dpad : Move source
- Right Stick : Rotation
- A : Toggle visibility
- B : Reset Position
- X : Reset Rotation
- Y : Reset Scale
- LB : Mirroir Scale X
- RB : Mirroir Scale Y
- LT : Zoom Out
- RT : Zoom In
- Start : Toggle on/off filter (last filter on the source)
- Select : Reset + exit

#### Example:
![](https://imgur.com/TFPo3kY.gif)
---

## 05 - Shake Source
Create a shake effect on a source

#### Script Configuration:
Edit the script and replace with your config
```
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
timer = 0.02
```
#### OBS Studio Configuration:
- Right click on the source and setup transformation settings to "No Bounds" and "Center alignement"

#### Usage :
- To start the script launch Shake_Source.py with a Streamdeck or with the Windows explorer
- To stop relaunch the script

---

## 06 - Disable_all_sources
Instant disables all sources on a scene. You can set an "exception list" to not disable certain sources

#### Script Configuration:
Edit the script and replace with your config
```
scene = "Scene_name"
exception_list = ["not_this_source", "not_this_one","not_me"]
host = "localhost"
port = 4444
password = "password"
```

#### Usage :
- To start the script launch Disable_all_sources.py with a Streamdeck or with the Windows explorer

---

## 07 - Sequence Sources
Toggle visibility for a sequence of sources, you can set it to Random or repeat or play once

#### Script Configuration:
Edit the script and replace with your config
```
########################################################################################
#######################################CONFIG BLOCK#####################################
scene = "Scene_name"
sources_list = ["01", "02", "03", "04", "05","06","07","08"]
transition_tempo = 0.1
random_mode = True #False : Sequence mode / True : Random Mode

repeat_mode = True #(Sequence mode only) False : Play sequence one time / True : Loop Mode for sequence
clean_sources_at_start = True #Disable all sources in list at start

host = "localhost"
port = 4444
password = "password"

toggle_txt = "Sequence_SOURCES_Toggle.txt"
rng_txt = "Sequence_SOURCES_RNG.txt"
########################################################################################
########################################################################################
```

#### Usage :
- To start the script launch Sequences_SOURCES.py with a Streamdeck or with the Windows explorer
- To stop relaunch the script (if repeat or random mode)

![](https://i.imgur.com/2kkTgPu.gif)

---

## Follow me :
- [@Prosperelucel](https://twitter.com/ProspereLucel)
- [Prospere on Twitch](https://twitch.tv/prospere)
- [My Discord](https://discord.gg/ac2xDrJ)

More to come
