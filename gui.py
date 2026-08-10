import customtkinter as ctk
import app_function as af
import json
import os
import threading
import voice
from PIL import Image, ImageTk
import pystray
saving_data_file = "data.json"
class Mainapp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')
        self.iconbitmap('picture\main_image.ico')
        self.my_font = ctk.CTkFont(family= "Segoe UI", size= 20)
        self.title("Customizable Assistant")
        self.geometry('340x410')
        self.configure(fg_color = 'white')
        self.label = ctk.CTkLabel(self, text= "Your personal assistant", font= self.my_font )
        self.label.pack(side = "top")
        self.buttn_frame = ctk.CTkFrame(self, 
                           bg_color= "transparent",
                           fg_color= '#FFFFFF')
        self.buttn_frame.pack(side = "top", pady = 20)
        self.start = ctk.CTkButton(self.buttn_frame, 
                            text= "Start", 
                            text_color= "#FFFFFF",
                            font= self.my_font,
                            width= 200,
                            height= 44,
                            corner_radius= 22,
                            border_width= 2, 
                            border_color= 'black',
                            command= self.start_stop
                            )

        self.start.pack(side = "top", pady = 20)
        self.command_list = ctk.CTkButton(self.buttn_frame, 
                            text= "Command list", 
                            text_color= "#FFFFFF",
                            font= self.my_font,
                            width= 200,
                            height= 44,
                            corner_radius= 22, 
                            border_width= 2,
                            border_color= 'black',
                            command= self.open_list
                            )
        self.command_list.pack(side = "top", pady = 20)
        self.customize = ctk.CTkButton(self.buttn_frame, 
                            text= "Customize", 
                            text_color= "#FFFFFF",
                            font= self.my_font,
                            width= 200,
                            height= 44,
                            corner_radius= 22, 
                            border_width= 2,
                            border_color= 'black',
                            command= self.open_customizing
                            )
        self.customize.pack(side = "top", pady = 20)
        self.user_guide = ctk.CTkButton(self.buttn_frame, 
                            text= "User guide", 
                            text_color= "#FFFFFF",
                            font= self.my_font,
                            width= 200,
                            height= 44,
                            corner_radius= 22, 
                            border_width= 2,
                            border_color= 'black',
                            command= self.open_user_guide
                            )
        self.user_guide.pack(side = "top", pady = 20)
        with open(saving_data_file, 'r', encoding= "utf-8") as file:
            data = json.load(file)
        if data['running_behind'] == 1:
            self.running_behind()
    def open_list(self):
        open_command_list(self)
    def running_behind(self):
        self.using_hide_window()
        self.protocol("WM_DELETE_WINDOW", self.turn_on_hide_window)
    def turn_on_hide_window(self):
        self.protocol("WM_DELETE_WINDOW", self.using_hide_window)
    def using_hide_window(self):
        image = Image.open(r"picture\main_image.png")
        self.withdraw()
        menu = (
            pystray.MenuItem("Mở ứng dụng", self.show_window, default=True),
            pystray.MenuItem("Thoát hoàn toàn", self.quit_app)
        )
        self.tray_icon = pystray.Icon("TkinterApp", image, "voice assistant", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    def show_window(self):
        if self.tray_icon:
            self.tray_icon.stop()  
        self.after(0, self.deiconify)    
    def quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.after(0, self.destroy)          
    def set_start(self):
        if voice.is_start:
            self.start.configure(text = 'Start')
            self.call_to_stop = 1
            voice.is_start = 0
            voice.is_begin = True
        self.after(200, self.set_start)
    def check_and_start(self):
        with open(saving_data_file, 'r', encoding= "utf-8") as file:
            data = json.load(file)
        if data['without_start'] == 1:
            self.start.configure(text = 'Stop')
            voice.call_to_stop = 0
            threading.Thread(target= af.start, daemon= True).start()
        if data['running_in_background'] == 1:
            self.turn_on_hide_window()
    def start_stop(self):
        if voice.call_to_stop:
            voice.call_to_stop = 0
            self.start.configure(text = "Stop")
            threading.Thread(target= af.start, daemon= True).start()
        else:
            voice.call_to_stop = 1
            self.start.configure(text = "Start")
            voice.is_begin = True
    def open_customizing(self):
        customizing_desktop(self)
    def open_user_guide(self):
        user_guide(self)
    def runnig_app(self):
        self.set_start()
        threading.Thread(target= self.check_and_start, daemon= True).start()
        self.mainloop()

#Adding buttons
class customizing_desktop(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.filename = "command_list.json"
        self.geometry('850x950+800+0')
        self.title("Customize")
        self.configure(fg_color = 'white')
        self.focus()
        self.iconbitmap('picture\customizing.ico')
        self.my_font = ctk.CTkFont(family= "Segoe UI", size= 20)
        with open(saving_data_file, 'r', encoding= 'utf-8') as file:
            data_start = json.load(file)
        self.start_check = ctk.IntVar(value= data_start['without_start'])
        self.hide = ctk.IntVar(value= data_start['running_in_background']) 
        self.behind = ctk.IntVar(value= data_start['running_behind'])
        #notice label
        self.notice_frame = ctk.CTkFrame(self, 
                                                bg_color= "transparent",
                                                fg_color= '#FFFFFF' )
        self.notice = ctk.CTkLabel(self.notice_frame,
                                    text= "***NOTICE: To know how to add or remove a command, " \
                                    "read this first: ",
                                    text_color= '#FF0000',
                                    font= ctk.CTkFont(
                                        family= "Segoe UI",
                                        size = 20,
                                        weight= 'bold'
                                    ))
        self.notice_buttn = ctk.CTkButton(self.notice_frame,
                                        text= "Open",
                                        width= 80,
                                        height= 35,
                                        corner_radius= 11,
                                        border_width= 1.5,
                                        border_color= 'black',
                                        command= self.open_user_guide)
        self.gen_frame = ctk.CTkFrame(self, 
                                        bg_color= "transparent",
                                        fg_color= '#FFFFFF' )
        self.gen_content = ctk.CTkLabel(self, 
                                text= "Command to turn the assistant on:",
                                font= self.my_font, 
                                )
        self.gen_entry = ctk.CTkEntry(
                            self.gen_frame,
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
        self.gen_buttn = ctk.CTkButton(self.gen_frame,
                                text= "Enter",
                                width= 80,
                                height= 35,
                                corner_radius= 11,
                                border_width= 1.5,
                                border_color= 'black',
                                command= self.getting_gen_entry)
        self.gen_warn = ctk.CTkLabel(self.gen_frame,
                                        text = "Successfully!!",
                                        font= self.my_font)
        #frame for exiting command
        self.exit_content = ctk.CTkLabel(self, 
                                    text= "Command to turn the assistant off:",
                                    font= self.my_font, 
                                    )
        self.exit_frame = ctk.CTkFrame(self, 
                                    bg_color= "transparent",
                                    fg_color= '#FFFFFF' )
        self.exit_entry = ctk.CTkEntry(
                                self.exit_frame,
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
        self.exit_buttn = ctk.CTkButton(self.exit_frame,
                                    text= "Enter",
                                    width= 80,
                                    height= 35,
                                    corner_radius= 11,
                                    border_width= 1.5,
                                    border_color= 'black',
                                    command= self.getting_exit_entry)
        self.gen_warn_del = ctk.CTkLabel(self.exit_frame,
                                                text = "Successfully!!",
                                                font= self.my_font)
        #frame for adding command
        self.add_content = ctk.CTkLabel(self, 
                                    text= "Adding your command:",
                                    font= self.my_font, 
                                    )
        self.add_frame = ctk.CTkFrame(self, 
                                        bg_color= "transparent",
                                        fg_color= '#FFFFFF' )
        self.add_warning = ctk.CTkLabel(self, 
                                    text= "Successfully!!",
                                    font= self.my_font,)
        self.sup_content = ctk.CTkLabel(self.add_frame, 
                                    text= "YOUR COMMAND" + 20 * " " + "TERMINAL COMMAND" ,
                                    font= ctk.CTkFont(
                                        family= 'consolas',
                                        size= 18
                                    ), 
                                    )
        self.add_your_entry = ctk.CTkEntry(
                                    self.add_frame,
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
        self.sep_content = ctk.CTkLabel(self.add_frame, 
                                    text= ":",
                                    font= ctk.CTkFont(
                                    family= "Consolas",
                                    size= 40,
                                    weight= 'bold'
                                        ), 
                                    )
        self.add_ter_entry = ctk.CTkEntry(
                                        self.add_frame,
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

        self.add_buttn = ctk.CTkButton(self.add_frame,
                                        text= "Add",
                                        width= 80,
                                        height= 35,
                                        corner_radius= 11,
                                        border_width= 1.5,
                                        border_color= 'black',
                                        command= self.getting_add_entry)
        
        #frame for removing command
        self.remove_content = ctk.CTkLabel(self, 
                                    text= "Remove your command",
                                        font= self.my_font, 
                                    )
        self.remove_frame = ctk.CTkFrame(self, 
                                bg_color= "transparent",
                                fg_color= '#FFFFFF' )
        self.remove_entry = ctk.CTkEntry(
                                    self.remove_frame,
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
        self.remove_buttn = ctk.CTkButton(self.remove_frame,
                                text= "Remove",
                                width= 80,
                                height= 35,
                                corner_radius= 11,
                                border_width= 1.5,
                                border_color= 'black',
                                command= self.getting_remove_entry)

        #frame for some settings
        self.wt_start_frame = ctk.CTkFrame(self, fg_color= 'white')
        self.run_without_start_buttn = ctk.CTkButton(self,
                                    text= "Save",
                                    width= 80,
                                    height= 35,
                                    corner_radius= 11,
                                    border_width= 1.5,
                                    border_color= 'black',
                                    command= self.saving_start)
        self.run_without_start_tick = ctk.CTkCheckBox(
            self.wt_start_frame,
            text= "Start assistant when opening app without pressing 'Start' button",
            variable= self.start_check
        )
        self.hide_window_tick = ctk.CTkCheckBox(
            self,
            text= "Allow assistant to run in the background (still pop up)",
            variable= self.hide
        )
        self.running_behind_tick = ctk.CTkCheckBox(
                    self,
                    text= "Allow app to run in background and not to pop up",
                    variable= self.behind
                )
        #warning label for remove
        self.remove_warn = ctk.CTkLabel(self.remove_frame,
                                text = "Successfully!!",
                                font= self.my_font)

        #list of command
        self.list_frame = ctk.CTkFrame(self, 
                                    bg_color= "transparent",
                                    fg_color= '#FFFFFF' )
        self.list_content = ctk.CTkLabel(self.list_frame, 
                                        text= "Open the list of command:",
                                        font= self.my_font, 
                                        )
        self.list_buttn = ctk.CTkButton(self.list_frame,
                                    text= "Open",
                                    width= 80,
                                    height= 35,
                                    corner_radius= 11,
                                    border_width= 1.5,
                                    border_color= 'black',
                                    command= self.cmd_list)

        #Json file
        self.son_frame = ctk.CTkFrame(self, 
                                        bg_color= "transparent",
                                        fg_color= '#FFFFFF' )
        self.son_content = ctk.CTkLabel(self.son_frame, 
                                            text= "Open JSON file:",
                                            font= self.my_font, 
                                            )
        self.son_buttn = ctk.CTkButton(self.son_frame,
                                        text= "Open",
                                        width= 80,
                                        height= 35,
                                        corner_radius= 11,
                                        border_width= 1.5,
                                        border_color= 'black',
                                        command= self.open_json)
        self.settings = ctk.CTkLabel(self,
                                     text = 'Some settings',
                                     font= self.my_font)
    #location
        self.notice_frame.pack(side = 'top', anchor = 'w')
        self.notice.pack(side = 'left')
        self.notice_buttn.pack(side = 'left')
    #gen_command
        self.gen_content.pack(side = 'top', anchor = 'w', pady = 5)
        self.gen_frame.pack(side = 'top', anchor = 'w', pady = 10)
        self.gen_entry.pack(padx = 10,anchor = 'w', side = 'left')
        self.gen_buttn.pack(side = 'left')
        self.gen_warn.pack_forget()
    #exit_command
        self.exit_content.pack(side = 'top', anchor = 'w', pady = 10)
        self.exit_frame.pack(side = 'top', anchor = 'w', pady = 10)
        self.exit_entry.pack(padx = 10,anchor = 'w', side = 'left')
        self.exit_buttn.pack(side = 'left')
        self.gen_warn_del.pack_forget()
    #add command
        self.add_content.pack(side = 'top', anchor = 'w', pady = 10)
        self.add_frame.pack(side = 'top', anchor = 'w', pady = 10)
        self.add_warning.pack_forget()
        self.sup_content.pack(side = 'top', anchor = 'w', padx = 60, pady = 5)
        self.add_your_entry.pack(padx = 10,anchor = 'w', side = 'left')
        self.sep_content.pack(side = 'left',  padx = 10)
        self.add_ter_entry.pack(padx = 10,anchor = 'w', side = 'left')
        self.add_buttn.pack(side = 'left', padx = 10)
    #remove command
        self.remove_content.pack(side = 'top', anchor = 'w', pady = 10)
        self.remove_frame.pack(side = 'top', anchor = 'w', pady = 10)
        self.remove_entry.pack(padx = 10,anchor = 'w', side = 'left')
        self.remove_buttn.pack(side = 'left')
        self.remove_warn.pack_forget()
        #list of command
        self.list_frame.pack(side = 'top', anchor = 'w', pady = 10)
        self.list_content.pack(side = 'left', anchor = 'w', pady = 10)
        self.list_buttn.pack(side = 'left', padx = 10)
    #Json file
        self.son_frame.pack(side = 'top', anchor = 'w', pady = 10)
        self.son_content.pack(side = 'left', anchor = 'w', pady = 10)
        self.son_buttn.pack(side = 'left', padx = 10)
    #run without start
        self.settings.pack(side = 'top', anchor = 'w', pady = 10)
        self.wt_start_frame.pack(side = 'top', anchor = 'w')
        self.run_without_start_tick.pack(side = 'left')
    #run in the background
        self.hide_window_tick.pack(side = 'top', anchor = 'w', pady = 5)
        self.running_behind_tick.pack(side = 'top', anchor = 'w', pady = 5)
        self.run_without_start_buttn.pack(side = 'top', anchor = 'w', pady =5)
    def open_user_guide(self):
        user_guide(self)
    def loading_json(self, user_command, ter_command):
        with open(self.filename, 'r', encoding= "utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
        data[user_command] = ter_command
        with open(self.filename, 'w', encoding= 'utf-8') as file:
            json.dump(data, file, ensure_ascii= False, indent= 4)
    def getting_gen_entry(self):
        cont = self.gen_entry.get()
        if cont == "":
            cont = 'waking up'
        elif any(char.isupper() for char in cont):
            self.gen_warn.configure(text = "Failed!! Uppercase is not allowed")
            self.gen_warn.pack(side = 'left', pady = 5)
            self.gen_warn.after(5000, self.gen_warn.pack_forget)
        elif any(char.isdigit() for char in cont):
            self.gen_warn.configure(text = "Failed!! Number is not allowed")
            self.gen_warn.pack(side = 'left', pady = 5)
            self.gen_warn.after(5000, self.gen_warn.pack_forget)
        else:
            self.loading_json("activating command", cont)
            self.gen_entry.delete(0, 'end')
            self.gen_warn.configure(text = "Successfully!!")
            self.gen_warn.pack(side = 'left', pady = 5)
            self.gen_warn.after(5000, self.gen_warn.pack_forget)
    def getting_exit_entry(self):
        cont = self.exit_entry.get()
        if cont == "":
            cont = "stop right now"
        elif any(char.isupper() for char in cont):
            self.gen_warn_del.configure(text = "Failed!! Uppercase is not allowed")
            self.gen_warn_del.pack(side = 'left', pady = 5)
            self.gen_warn_del.after(5000, self.gen_warn_del.pack_forget)
        elif any(char.isdigit() for char in cont):
            self.gen_warn_del.configure(text = "Failed!! Number is not allowed")
            self.gen_warn_del.pack(side = 'left', pady = 5)
            self.gen_warn_del.after(5000, self.gen_warn_del.pack_forget)
        else: 
            self.loading_json("exiting command", cont)
            self.exit_entry.delete(0, 'end')
            self.gen_warn_del.configure(text = "Successfully!!")
            self.gen_warn_del.pack(side = 'left', pady = 5)
            self.gen_warn_del.after(5000, self.gen_warn_del.pack_forget)
    def getting_add_entry(self):
        add_your_command = self.add_your_entry.get()
        add_ter_command = self.add_ter_entry.get()
        if any(char.isupper() for char in add_your_command):
            self.add_warning.configure(text = "Failed!! Uppercase is not allowed")
            self.add_warning.pack(after = self.add_frame, pady = 5)
            self.add_warning.after(5000, self.add_warning.pack_forget)
        elif any(char.isdigit() for char in add_your_command):
            self.add_warning.configure(text = "Failed!! Number is not allowed")
            self.add_warning.pack(after = self.add_frame, pady = 5)
            self.add_warning.after(5000, self.add_warning.pack_forget)
        elif add_your_command != "" and add_ter_command != "":
            self.loading_json(add_your_command, add_ter_command)
            self.add_your_entry.delete(0, 'end')
            self.add_ter_entry.delete(0, 'end')
            self.add_warning.configure(text = "Successfully!!")
            self.add_warning.pack(after = self.add_frame, pady = 5)
            self.add_warning.after(5000, self.add_warning.pack_forget)
    def getting_remove_entry(self):
        remove_command = self.remove_entry.get()
        with open(self.filename, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
        if remove_command in current_data:
            current_data.pop(remove_command, None)
            self.remove_entry.delete(0, 'end')
            self.remove_warn.configure(text = "Successfully!!")
            self.remove_warn.pack(side = "left", padx =5 )
            self.remove_warn.after(5000, self.remove_warn.pack_forget)
        else:
            print("Unsuccessfully!!, command doesn't exist")
            self.remove_warn.configure(text = "Unsuccessfully!!, command doesn't exist")
            self.remove_warn.pack(side = 'left', padx = 5)
            self.remove_warn.after(5000, self.remove_warn.pack_forget)
        with open(self.filename, 'w', encoding= 'utf-8') as file:
            json.dump(current_data, file, ensure_ascii= False, indent= 4)
    def open_json(self):
        os.startfile(self.filename)
    def saving_start(self):
        with open(saving_data_file, 'r', encoding= 'utf-8') as file:
            data = json.load(file)
        data["without_start"] = self.start_check.get()
        data["running_in_background"] = self.hide.get()
        data['running_behind'] = self.behind.get()
        with open(saving_data_file, 'w', encoding= 'utf-8') as file:
            json.dump(data, file, ensure_ascii= False, indent= 4)
    def cmd_list(self):
        open_command_list(self)
class open_command_list(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('450x550+200+100')
        self.filename = "command_list.json"
        self.title("List of commands")
        self.iconbitmap('picture\command_list.ico')
        self.my_font = ctk.CTkFont(family= "Segoe UI", size= 20)
        self.configure(fg_color = 'white')
        self.focus()
        with open(self.filename, 'r', encoding= 'utf-8') as file:
            cur_data = json.load(file)
        self.open_text = ctk.CTkLabel(self,
                                text= "Opening & Exiting command:",
                                font= self.my_font)
        self.open_text.pack(side = "top")
        self.activating = ctk.CTkLabel(self,
                                text= f"activating command --> {cur_data['activating command']}",
                                font= self.my_font)
        self.activating.pack(side = 'top')
        self.exiting = ctk.CTkLabel(self,
                                text= f"exiting command --> {cur_data['exiting command']}", 
                                font= self.my_font)
        self.exiting.pack(side = 'top')
        self.list_of_command = ctk.CTkScrollableFrame(self,
                                    border_color= 'black',
                                    border_width= 2,
                                    label_text= "LIST OF COMMANDS",
                                    label_font= self.my_font)
        self.list_of_command.pack(side='top', fill='both', expand=True, padx=10, pady=10)
        self.list_of_command.grid_columnconfigure(0, weight=1)
        self.list_of_command.grid_columnconfigure(1, weight=1)
        self.your_command = ctk.CTkLabel(self.list_of_command, text="YOUR COMMAND", font= self.my_font)
        self.your_command.grid(row=0, column=0, padx=10, pady=5) 
        self.ter_command = ctk.CTkLabel(self.list_of_command, text="TERMINAL COMMAND", font= self.my_font)
        self.ter_command.grid(row=0, column=1, padx=10, pady=5) 
        real_data = {k: v for k, v in cur_data.items() if k not in ['activating command', 'exiting command']}
        for row_idx, (k, v) in enumerate(real_data.items(), start=1):
            self.key = ctk.CTkLabel(self.list_of_command, text=f'{k}', font= self.my_font)
            self.key.grid(row=row_idx, column=0, padx=10, pady=2)
            self.value = ctk.CTkLabel(self.list_of_command, text=f'{v}', font= self.my_font)
            self.value.grid(row=row_idx, column=1, padx=10, pady=2)
class user_guide(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('1650x1050+0+0')
        self.iconbitmap(r'picture\user_guide.ico')
        self.title('User guide')
        self.my_font = ctk.CTkFont(family= "Segoe UI", size= 20, weight= 'bold')
        self.l_font = ctk.CTkFont(family= "Segoe UI", size= 14)
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            width=1650, 
            height=1050,
            label_text="USER GUIDE",
            label_font= self.l_font
            
        )
        self.other_font = ctk.CTkFont(family= "Segoe UI", size= 17)
        self.other_font_h = ctk.CTkFont(family= "Segoe UI", size= 19, weight= 'bold')
        self.label = ctk.CTkLabel(self.scroll_frame,text = 'Below is the user guide of this app, read it carefully before using:'
                                  , font= self.my_font)
        self.first = ctk.CTkLabel(self.scroll_frame, text = 'I. How to change the activating command and deactivating command', 
                                  font= self.my_font)
        self.first_conton = ctk.CTkLabel(self.scroll_frame, text = '1. Activating command:', font= self.other_font_h)
        self.first_contoff = ctk.CTkLabel(self.scroll_frame, text = '2. Deactivating command:', font = self.other_font_h)
        self.second = ctk.CTkLabel(self.scroll_frame, text = 'II. How to add and remove the command', font= self.my_font)
        self.second_one = ctk.CTkLabel(self.scroll_frame, text = '1. Add the command',font = self.other_font_h)
        self.second_cont = ctk.CTkLabel(self.scroll_frame, text = "This step is really important because " \
                                        "if you don't have any command in the command list," \
                                        "assistant can't work, so here is how to add the command:",font = self.other_font)
        self.second_add = ctk.CTkLabel(self.scroll_frame, text = "First, you have to write your command",font = self.other_font)
        self.second_continue = ctk.CTkLabel(self.scroll_frame, text = "Now you have to search Google with the syntax 'How to .... by Powershell'. " \
                                            "Copy the code and Paste into the terminal command ",font = self.other_font)
        self.second_ex = ctk.CTkLabel(self.scroll_frame, text = "Ex: If I want to open chrome whenever I say 'open chrome'. So now I write the command " \
        "'open chrome' in the your command and search google 'How to open chrome by PowerShell',",font = self.other_font)
        self.second_bonus = ctk.CTkLabel(self.scroll_frame, text = "the result is 'start chrome', I copy this code and paste it into the terminal commmand. Done!!", font= self.other_font)
        self.second_two = ctk.CTkLabel(self.scroll_frame, text = '2. Remove the command:',font = self.other_font_h)
        self.second_three = ctk.CTkLabel(self.scroll_frame, text = 'III. Other settings', font= self.my_font)
        self.more = ctk.CTkLabel(self.scroll_frame, text = 'If you want to double check your command and the activating, deactivating command, ' \
        'you can open the command list to see them again',font = self.other_font)
        self.another_option = ctk.CTkLabel(self.scroll_frame, text = "If you know how to use the json file, you can use this to change, add or remove your commands " \
        "much quickly", font = self.other_font)
        self.another_option_cont = ctk.CTkLabel(self.scroll_frame, text = "in case you change this json file and the app goes wrong, you only need to delate this json file, the app will "  \
        "create another original file for you", font = self.other_font)
        self.some_setting = ctk.CTkLabel(self.scroll_frame, text = "you can also see some settings in the bottom, I think you can easily understand them or you can test these settings," \
        "remeber to press 'save' button and restart the app to apply the changes.",font = self.other_font)
        self.open_image = ctk.CTkImage(light_image= Image.open(r'picture\open_app.png'),
                                  dark_image= Image.open(r'picture\open_app.png'),
                                  size= (592,226))
        self.open_img = ctk.CTkLabel(self.scroll_frame, image= self.open_image, text= '')
        self.close_image = ctk.CTkImage(light_image= Image.open(r'picture\close_app.png'),
                                  dark_image= Image.open(r'picture\close_app.png'),
                                  size= (592,226))
        self.close_img = ctk.CTkLabel(self.scroll_frame, image= self.close_image, text= '')
        self.remove_image = ctk.CTkImage(light_image= Image.open(r'picture\remove.png'),
                                  dark_image= Image.open(r'picture\remove.png'),
                                  size= (592,226))
        self.remove_img = ctk.CTkLabel(self.scroll_frame, image= self.remove_image, text= '')
        self.add_image = ctk.CTkImage(light_image= Image.open(r'picture\add.png'),
                                  dark_image= Image.open(r'picture\add.png'),
                                  size= (592,226))
        self.add_img = ctk.CTkLabel(self.scroll_frame, image= self.add_image, text= '')
        self.label.pack(side = 'top', pady = 5, anchor = 'w')
        self.scroll_frame.pack(fill="x", expand=True)
        self.first.pack(side = 'top', pady = 5, anchor = 'w')
        self.first_conton.pack(side = 'top', pady = 5, anchor = 'w')
        self.open_img.pack(side = 'top', pady = 5, anchor = 'w')
        self.first_contoff.pack(side = 'top', pady = 5, anchor = 'w')
        self.close_img.pack(side = 'top', pady = 5, anchor = 'w')
        self.second.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_one.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_cont.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_add.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_continue.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_ex.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_bonus.pack(side = 'top', pady = 5, anchor = 'w')
        self.add_img.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_two.pack(side = 'top', pady = 5, anchor = 'w')
        self.remove_img.pack(side = 'top', pady = 5, anchor = 'w')
        self.second_three.pack(side = 'top', pady = 5, anchor = 'w')
        self.more.pack(side = 'top', pady = 5, anchor = 'w')
        self.another_option.pack(side = 'top', pady = 5, anchor = 'w')
        self.another_option_cont.pack(side = 'top', pady = 5, anchor = 'w')
        self.some_setting.pack(side = 'top', pady = 5, anchor = 'w')
        self.after(100, self.focus_set)
app = Mainapp()
app.runnig_app()