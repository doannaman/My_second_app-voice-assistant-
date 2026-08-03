import voice
import json
import os
filename = "command_list.json"
#initializing json file
if not os.path.exists(filename):
    initial = {
        "activating command" : "waking up",
        "exiting command": "stop right now"
    }
    with open(filename, 'w', encoding= 'utf-8') as file:
        json.dump(initial, file, ensure_ascii= False, indent= 4 )
    print("đã khởi tạo file thành công")
#loading json file
def start():
    with open(filename, 'r', encoding= "utf-8") as file:
        data = json.load(file)
    begin = data["activating command"]
    exit = data["exiting command"]
    voice.running_backend(opening_command = begin,
                          exiting_command= exit)


