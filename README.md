# Prospere Obs studio dirty scripts
Collection of dirty python script for Open Broadcast software.
I'm not a professional developper, I do this on my free time for friends, I'm just a French guy who love "la bidouille" :)

Important : Currently most of the script will NOT work in "Studio mode".


### Requirement :
- Windows 10
- [OBS Studio](https://obsproject.com/)
- [Python27](https://www.python.org/ftp/python/2.7/python-2.7.amd64.msi)
- [obs-websocket](https://github.com/Palakis/obs-websocket) from [@LePalakis](https://twitter.com/LePalakis)
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) from Guillaume Genty a.k.a Elektordi


### Python27 Installation and dependencies : 
- Install Python27
- Open command prompt or a terminal (windows key + R, type "cmd" and enter)
- Go to your Python27 folder in the command prompt (cd c:\Python27)

All the script requiere the python library obs-websocket-py
- type in the cmd

```
python.exe -m pip install obs-websocket-py
```

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

## Sequence Scene
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

## Freeze Frame
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


More to come
