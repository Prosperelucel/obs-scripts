import os
import sys
from Sequence_SCENES_Config import toggle_txt
# set dir to script folder
os.chdir(sys.path[0])

toggle = 0
toggle_file = open(toggle_txt, "w")
toggle_file.write('{}'.format(toggle))
toggle_file.close()

