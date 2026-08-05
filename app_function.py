import voice
import json
import os
filename = "command_list.json"
saving_file = "data.json"
#initializing json file
if not os.path.exists(filename):
    initial = {
        "activating command" : "waking up",
        "exiting command": "stop right now"
    }
    with open(filename, 'w', encoding= 'utf-8') as file:
        json.dump(initial, file, ensure_ascii= False, indent= 4 )
    print("đã khởi tạo file thành công")
if not os.path.exists(saving_file):
    init = {"without_start" : 0}
    with open(saving_file, 'w', encoding= 'utf-8') as file:
        json.dump(init, file, ensure_ascii= False, indent= 4 )
#loading json file
def start(call_to_stop):
    with open(filename, 'r', encoding= "utf-8") as file:
        data = json.load(file)
    begin = data["activating command"]
    exit = data["exiting command"]
    if begin == "":
        begin = "waking up",
    if exit == "":
        exit = "stop right now"
    begin_exit = ["activating command", "exiting command"]
    cmd_list = {k:v for k,v in data.items() if k not in begin_exit}
    print(cmd_list)
    voice.running_backend(opening_command = begin,
                          exiting_command= exit,
                          listofcommand= cmd_list,
                          calltostop= call_to_stop)

