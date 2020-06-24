# obs-scripts
Collection of dirty python script for Open Broadcast software.

Important : Currently most of the script will NOT work in "Studio mode".

### Requirement :
- Windows 10
- [OBS Studio](https://obsproject.com/)
- [Python27](https://www.python.org/ftp/python/2.7/python-2.7.amd64.msi)
- [obs-websocket](https://github.com/Palakis/obs-websocket) from [@LePalakis](https://twitter.com/LePalakis)
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) from Guillaume Genty a.k.a Elektordi

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
