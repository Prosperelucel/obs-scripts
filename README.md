# obs-scripts
Collection of python script for Open Broadcast software

### Requirement :
- Windows 10 
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

More to come
