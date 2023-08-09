# -*- coding: utf-8 -*-
import json
from io import open
import pprint
import sys

# reload(sys)

# j_path = r'I:\projects\nzt\shot\n80\n80190\ani\n80190.ani.blocking.v002\shot_components.json'
# print(sys.version)
# collect = []
# repeat = 0
# with open(j_path, 'r', encoding="utf-8") as f:
#     my_json = json.load(f)
#     for i in my_json.keys():
#         iterm = i.decode() #type:str
#         if ':' in iterm:
#             iterm = ''.join(iterm.split(':')[0:2])
#         for j in collect:
#             if j == iterm:
#                 repeat += 1
#             else:
#                 collect.append(iterm)
# print(repeat)
convert_input = os.getenv("temp") + "/oct_publish/" + "t.mov"
convert_output = os.getenv("temp") + "/oct_publish/" + "test.mov"
convert_output = convert_output.replace('/', '\\')
convert_input = convert_input.replace('/', '\\')
convert_command = "rez-env ffmpeg -- ffmpeg -i {} -strict experimental -vcodec libx264 -pix_fmt yuv420p -g 30 -vprofile high -bf 0 -crf 23 {}"\
                .format(convert_input, convert_output)
import subprocess
sp = subprocess.Popen(convert_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
sp.communicate()
print("OK!!!!")