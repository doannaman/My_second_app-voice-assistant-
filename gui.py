import customtkinter as ctk
import app_function as af
import json
import os
import threading
import voice
filename = "command_list.json"
saving_data_file = "data.json"
#start_stop function
call_to_stop = 1
def start_stop():
    global call_to_stop
    if call_to_stop:
        call_to_stop = 0
        start.configure(text = "Stop")
        threading.Thread(target= lambda: af.start(call_to_stop = 0), daemon= True).start()
    else:
        call_to_stop = 1
        start.configure(text = "Start")
        voice.is_begin = True
        threading.Thread(target= lambda: af.start(call_to_stop = 1), daemon= True).start()
#input json file 
def loading_json(user_command, ter_command):
    with open(filename, 'r', encoding= "utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    data[user_command] = ter_command
    with open(filename, 'w', encoding= 'utf-8') as file:
        json.dump(data, file, ensure_ascii= False, indent= 4)
root = ctk.CTk()
#Setting the background for the app
ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')
root.title("Customizable Assistant")
root.geometry('340x410')
root.configure(fg_color = 'white')
#my font
my_font = ctk.CTkFont(family= "Segoe UI", size= 20)
label = ctk.CTkLabel(root, text= "Your personal assistant", font= my_font )
label.pack(side = "top")
#Adding buttons
class customizing_desktop:
    def __init__(self):
        self.window = ctk.CTkToplevel(root)
        
    def config_desktop(self):
        self.window.geometry('850x950+800+0')
        self.window.title("Customize")
        self.window.configure(fg_color = 'white')
        self.window.focus()
    def getting_gen_entry():
        cont = gen_entry.get()
        if cont == "":
            cont = 'waking up'
        else:
            loading_json("activating command", cont)
            gen_entry.delete(0, 'end')
    def getting_exit_entry():
        cont = exit_entry.get()
        if cont == "":
            cont = "stop right now"
        else: 
            loading_json("exiting command", cont)
            exit_entry.delete(0, 'end')
    def getting_add_entry():
        add_your_command = add_your_entry.get()
        add_ter_command = add_ter_entry.get()
        if add_your_command != "" and add_ter_command != "":
            loading_json(add_your_command, add_ter_command)
            add_your_entry.delete(0, 'end')
            add_ter_entry.delete(0, 'end')
            add_warning.configure(text = "Successfully!!")
            add_warning.pack(after = add_frame, pady = 5)
            add_warning.after(5000, add_warning.pack_forget)
    def getting_remove_entry():
        remove_command = remove_entry.get()
        with open(filename, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
        if remove_command in current_data:
            current_data.pop(remove_command, None)
            remove_entry.delete(0, 'end')
            remove_warn.configure(text = "Successfully!!")
            remove_warn.pack(side = "left", padx =5 )
            remove_warn.after(5000, remove_warn.pack_forget)
        else:
            print("Unsuccessfully!!, command doesn't exist")
            remove_warn.configure(text = "Unsuccessfully!!, command doesn't exist")
            remove_warn.pack(side = 'left', padx = 5)
            remove_warn.after(5000, remove_warn.pack_forget)
        with open(filename, 'w', encoding= 'utf-8') as file:
            json.dump(current_data, file, ensure_ascii= False, indent= 4)
    def open_json():
        os.startfile(filename)
        #without starting
        with open(saving_data_file, 'r', encoding= 'utf-8') as file:
            data_start = json.load(file)
        start_check = ctk.IntVar(value= data_start['without_start'])
    def customize_desktop(self):
        self.config_desktop()
        self.getting_gen_entry()
        self.getting_exit_entry()
        self.getting_add_entry()
        self.getting_remove_entry()
        self.open_json()
        
        
        def saving_start():
            with open(saving_data_file, 'r', encoding= 'utf-8') as file:
                data = json.load(file)
            data["without_start"] = start_check.get()
            with open(saving_data_file, 'w', encoding= 'utf-8') as file:
                json.dump(data, file, ensure_ascii= False, indent= 4)
        #command_list    
        def open_command_list():
                cmd_list = ctk.CTkToplevel(window)
                cmd_list.geometry('450x550+200+100')
                cmd_list.title("List of commands")
                cmd_list.configure(fg_color = 'white')
                cmd_list.focus()
                with open(filename, 'r', encoding= 'utf-8') as file:
                    cur_data = json.load(file)
                open_text = ctk.CTkLabel(cmd_list,
                                        text= "Opening & Exiting command:",
                                        font= my_font)
                open_text.pack(side = "top")
                activating = ctk.CTkLabel(cmd_list,
                                        text= f"activating command --> {cur_data['activating command']}",
                                        font= my_font)
                activating.pack(side = 'top')
                exiting = ctk.CTkLabel(cmd_list,
                                        text= f"exiting command --> {cur_data['exiting command']}", 
                                        font= my_font)
                exiting.pack(side = 'top')
                list_of_command = ctk.CTkScrollableFrame(cmd_list,
                                            border_color= 'black',
                                            border_width= 2,
                                            label_text= "LIST OF COMMANDS",
                                            label_font= my_font)
                list_of_command.pack(side='top', fill='both', expand=True, padx=10, pady=10)
                list_of_command.grid_columnconfigure(0, weight=1)
                list_of_command.grid_columnconfigure(1, weight=1)
                your_command = ctk.CTkLabel(list_of_command, text="YOUR COMMAND", font=my_font)
                your_command.grid(row=0, column=0, padx=10, pady=5) 
                ter_command = ctk.CTkLabel(list_of_command, text="TERMINAL COMMAND", font=my_font)
                ter_command.grid(row=0, column=1, padx=10, pady=5) 
                real_data = {k: v for k, v in cur_data.items() if k not in ['activating command', 'exiting command']}
                for row_idx, (k, v) in enumerate(real_data.items(), start=1):
                    key = ctk.CTkLabel(list_of_command, text=f'{k}', font=my_font)
                    key.grid(row=row_idx, column=0, padx=10, pady=2)
                    value = ctk.CTkLabel(list_of_command, text=f'{v}', font=my_font)
                    value.grid(row=row_idx, column=1, padx=10, pady=2)
        #notice
        notice = ctk.CTkLabel(window,
                            text= "***NOTICE: To know how to add or remove a command, " \
                            "read this first: ",
                            text_color= '#FF0000',
                            font= ctk.CTkFont(
                                family= "Segoe UI",
                                size = 20,
                                weight= 'bold'
                            ))

        #frame for generate command
        gen_frame = ctk.CTkFrame(window, 
                                bg_color= "transparent",
                                fg_color= '#FFFFFF' )
        gen_content = ctk.CTkLabel(window, 
                                text= "Command to turn the assistant on:",
                                font= my_font, 
                                )
        gen_entry = ctk.CTkEntry(
                            gen_frame,
                            placeholder_text="Write a command here", 
                            width=250,                  
                            height=40,                  
                            corner_radius=20,           
                            border_width=1.5,
                            border_color="black",       
                            fg_color="#F0F0F0",         
                            text_color="black",         
                            placeholder_text_color="gray" 
                        )
        gen_buttn = ctk.CTkButton(gen_frame,
                                text= "Enter",
                                width= 80,
                                height= 35,
                                corner_radius= 11,
                                border_width= 1.5,
                                border_color= 'black',
                                command= getting_gen_entry)

        #frame for exiting command
        exit_content = ctk.CTkLabel(window, 
                                    text= "Command to turn the assistant off:",
                                    font= my_font, 
                                    )
        exit_frame = ctk.CTkFrame(window, 
                                    bg_color= "transparent",
                                    fg_color= '#FFFFFF' )
        exit_entry = ctk.CTkEntry(
                                exit_frame,
                                placeholder_text="Write a command here", 
                                width=250,                  
                                height=40,                  
                                corner_radius=20,           
                                border_width=1.5,
                                border_color="black",       
                                fg_color="#F0F0F0",         
                                text_color="black",         
                                placeholder_text_color="gray" 
                            )
        exit_buttn = ctk.CTkButton(exit_frame,
                                    text= "Enter",
                                    width= 80,
                                    height= 35,
                                    corner_radius= 11,
                                    border_width= 1.5,
                                    border_color= 'black',
                                    command= getting_exit_entry)
        
        #frame for adding command
        add_content = ctk.CTkLabel(window, 
                                    text= "Adding your command:",
                                    font= my_font, 
                                    )
        add_frame = ctk.CTkFrame(window, 
                                        bg_color= "transparent",
                                        fg_color= '#FFFFFF' )
        add_warning = ctk.CTkLabel(window, 
                                    text= "Successfully!!",
                                    font= my_font,)
        sup_content = ctk.CTkLabel(add_frame, 
                                    text= "Your command" + 28 * " " + "Terminal command" ,
                                    font= my_font, 
                                    )
        add_your_entry = ctk.CTkEntry(
                                    add_frame,
                                    placeholder_text="Write your command here", 
                                    width=250,                  
                                    height=40,                  
                                    corner_radius=20,           
                                    border_width=1.5,
                                    border_color="black",       
                                    fg_color="#F0F0F0",         
                                    text_color="black",         
                                    placeholder_text_color="gray" 
                                )
        sep_content = ctk.CTkLabel(add_frame, 
                                    text= ":",
                                    font= ctk.CTkFont(
                                    family= "Consolas",
                                    size= 40,
                                    weight= 'bold'
                                        ), 
                                    )
        add_ter_entry = ctk.CTkEntry(
                                        add_frame,
                                        placeholder_text="Write terminal command here", 
                                        width=250,                  
                                        height=40,                  
                                        corner_radius=20,           
                                        border_width=1.5,
                                        border_color="black",       
                                        fg_color="#F0F0F0",         
                                        text_color="black",         
                                        placeholder_text_color="gray" 
                                    )
    
        add_buttn = ctk.CTkButton(add_frame,
                                        text= "Add",
                                        width= 80,
                                        height= 35,
                                        corner_radius= 11,
                                        border_width= 1.5,
                                        border_color= 'black',
                                        command= getting_add_entry)
        
        #frame for removing command
        remove_content = ctk.CTkLabel(window, 
                                    text= "Remove your command",
                                        font= my_font, 
                                    )
        remove_frame = ctk.CTkFrame(window, 
                                bg_color= "transparent",
                                fg_color= '#FFFFFF' )
        remove_entry = ctk.CTkEntry(
                                    remove_frame,
                                    placeholder_text="Write a command here", 
                                    width=250,                  
                                    height=40,                  
                                    corner_radius=20,           
                                    border_width=1.5,
                                    border_color="black",       
                                    fg_color="#F0F0F0",         
                                    text_color="black",         
                                    placeholder_text_color="gray" 
                                )
        remove_buttn = ctk.CTkButton(remove_frame,
                                text= "Remove",
                                width= 80,
                                height= 35,
                                corner_radius= 11,
                                border_width= 1.5,
                                border_color= 'black',
                                command= getting_remove_entry)

        #frame for some settings
        wt_start_frame = ctk.CTkFrame(window, fg_color= 'white')
        run_without_start_buttn = ctk.CTkButton(wt_start_frame,
                                    text= "Save",
                                    width= 80,
                                    height= 35,
                                    corner_radius= 11,
                                    border_width= 1.5,
                                    border_color= 'black',
                                    command= saving_start)
        run_without_start_tick = ctk.CTkCheckBox(
            wt_start_frame,
            text= "Start assistant when opening app without pressing 'Start' button",
            variable= start_check
        )

        #warning label for remove
        remove_warn = ctk.CTkLabel(remove_frame,
                                text = "Successfully!!",
                                font= my_font)

        #list of command
        list_frame = ctk.CTkFrame(window, 
                                    bg_color= "transparent",
                                    fg_color= '#FFFFFF' )
        list_content = ctk.CTkLabel(list_frame, 
                                        text= "Your list of command:",
                                        font= my_font, 
                                        )
        list_buttn = ctk.CTkButton(list_frame,
                                    text= "List",
                                    width= 80,
                                    height= 35,
                                    corner_radius= 11,
                                    border_width= 1.5,
                                    border_color= 'black',
                                    command= open_command_list)

        #Json file
        son_frame = ctk.CTkFrame(window, 
                                        bg_color= "transparent",
                                        fg_color= '#FFFFFF' )
        son_content = ctk.CTkLabel(son_frame, 
                                            text= "Open JSON file to add or remove commands manually:",
                                            font= my_font, 
                                            )
        son_buttn = ctk.CTkButton(son_frame,
                                        text= "Open JSON file",
                                        width= 80,
                                        height= 35,
                                        corner_radius= 11,
                                        border_width= 1.5,
                                        border_color= 'black',
                                        command= open_json)
        #Location for each part
            
            #notice label
        notice.pack(side = 'top', anchor = 'w')

            #gen_command
        gen_content.pack(side = 'top', anchor = 'w', pady = 10)
        gen_frame.pack(side = 'top', anchor = 'w', pady = 10)
        gen_entry.pack(padx = 10,anchor = 'w', side = 'left')
        gen_buttn.pack(side = 'left')

            #exit_command
        exit_content.pack(side = 'top', anchor = 'w', pady = 10)
        exit_frame.pack(side = 'top', anchor = 'w', pady = 10)
        exit_entry.pack(padx = 10,anchor = 'w', side = 'left')
        exit_buttn.pack(side = 'left')

            #add command
        add_content.pack(side = 'top', anchor = 'w', pady = 10)
        add_frame.pack(side = 'top', anchor = 'w', pady = 10)
        add_warning.pack_forget()
        sup_content.pack(side = 'top', anchor = 'w', padx = 60, pady = 10)
        add_your_entry.pack(padx = 10,anchor = 'w', side = 'left')
        sep_content.pack(side = 'left',  padx = 10)
        add_ter_entry.pack(padx = 10,anchor = 'w', side = 'left')
        add_buttn.pack(side = 'left', padx = 10)

            #remove command
        remove_content.pack(side = 'top', anchor = 'w', pady = 10)
        remove_frame.pack(side = 'top', anchor = 'w', pady = 10)
        remove_entry.pack(padx = 10,anchor = 'w', side = 'left')
        remove_buttn.pack(side = 'left')
        remove_warn.pack_forget()
    
                #list of command
        list_frame.pack(side = 'top', anchor = 'w', pady = 10)
        list_content.pack(side = 'left', anchor = 'w', pady = 10, padx = 20)
        list_buttn.pack(side = 'left')

            #Json file
        son_frame.pack(side = 'top', anchor = 'w', pady = 10)
        son_content.pack(side = 'left', anchor = 'w', pady = 10, padx = 20)
        son_buttn.pack(side = 'left')

            #run without start
        wt_start_frame.pack(side = 'top', anchor = 'w')
        run_without_start_tick.pack(side = 'left')
        run_without_start_buttn.pack(side = 'left', pady =5)
        
#button frame
buttn_frame = ctk.CTkFrame(root, 
                           bg_color= "transparent",
                           fg_color= '#FFFFFF')
buttn_frame.pack(side = "top", pady = 20)
start = ctk.CTkButton(buttn_frame, 
                      text= "Start", 
                      text_color= "#FFFFFF",
                      font= my_font,
                      width= 200,
                      height= 44,
                      corner_radius= 22,
                      border_width= 2, 
                      border_color= 'black',
                      command= start_stop
                      )

start.pack(side = "top", pady = 20)
def set_start():
    global call_to_stop
    if voice.is_start:
        start.configure(text = 'Start')
        call_to_stop = 1
        voice.is_start = 0
        voice.is_begin = True
    root.after(200, set_start)
set_start()
command_list = ctk.CTkButton(buttn_frame, 
                      text= "Command list", 
                      text_color= "#FFFFFF",
                      font= my_font,
                      width= 200,
                      height= 44,
                      corner_radius= 22, 
                      border_width= 2,
                      border_color= 'black',
                      )
command_list.pack(side = "top", pady = 20)
customize = ctk.CTkButton(buttn_frame, 
                      text= "Customize", 
                      text_color= "#FFFFFF",
                      font= my_font,
                      width= 200,
                      height= 44,
                      corner_radius= 22, 
                      border_width= 2,
                      border_color= 'black',
                      command= customizing_desktop.customize_desktop
                      )
customize.pack(side = "top", pady = 20)
user_guide = ctk.CTkButton(buttn_frame, 
                      text= "User guide", 
                      text_color= "#FFFFFF",
                      font= my_font,
                      width= 200,
                      height= 44,
                      corner_radius= 22, 
                      border_width= 2,
                      border_color= 'black'
                      )
user_guide.pack(side = "top", pady = 20)
#for customizing
def check_and_start():
    with open(saving_data_file, 'r', encoding= "utf-8") as file:
        data = json.load(file)
    if data['without_start'] == 1:
        start.configure(state = 'disabled')
        af.start(call_to_stop= 0)
threading.Thread(target= check_and_start, daemon= True).start()
root.mainloop()
