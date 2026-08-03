import customtkinter as ctk
import app_function as af
import json
filename = "command_list.json"
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
def customize_desktop():
    window = ctk.CTkToplevel(root)
    window.geometry('850x950+800+0')
    window.title("Customize")
    window.configure(fg_color = 'white')
    window.focus()
    #function to get info
    def getting_gen_entry():
        cont = gen_entry.get()
        if cont == "":
            cont = 'waking up'
        else:
            loading_json("activating command", cont)
            gen_entry.delete(0, 'end')
    def getting_exit_entry():
        if cont == "":
           cont = "stop right now"
        else: 
            cont = exit_entry.get()
            loading_json("exiting command", cont)
            exit_entry.delete(0, 'end')
    def getting_add_entry():
        if add_your_command == "" or add_ter_command == "":
            print("Unsuccessfully, you may have not filled yet")
        else:
            add_your_command = add_your_entry.get()
            add_ter_command = add_ter_entry.get()
            loading_json(add_your_command, add_ter_command)
            add_your_entry.delete(0, 'end')
            add_ter_entry.delete(0, 'end')
    def getting_remove_entry():
        remove_command = remove_entry.get()
        with open(filename, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
        if remove_command in current_data:
            current_data.pop(remove_command, None)
            remove_entry.delete(0, 'end')
        else:
            print("command doesn't exist, try again")
        with open(filename, 'w', encoding= 'utf-8') as file:
            json.dump(current_data, file, ensure_ascii= False, indent= 4)

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
                                   border_color= 'black')

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
                                       border_color= 'black')
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
    add_frame.pack(side = 'top', anchor = 'w')
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

        #list of command
    list_frame.pack(side = 'top', anchor = 'w', pady = 10)
    list_content.pack(side = 'left', anchor = 'w', pady = 10, padx = 20)
    list_buttn.pack(side = 'left')

        #Json file
    son_frame.pack(side = 'top', anchor = 'w', pady = 10)
    son_content.pack(side = 'left', anchor = 'w', pady = 10, padx = 20)
    son_buttn.pack(side = 'left')
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
                      command= af.start
                      )
start.pack(side = "top", pady = 20)
command_list = ctk.CTkButton(buttn_frame, 
                      text= "Command list", 
                      text_color= "#FFFFFF",
                      font= my_font,
                      width= 200,
                      height= 44,
                      corner_radius= 22, 
                      border_width= 2,
                      border_color= 'black'
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
                      command= customize_desktop
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

root.mainloop()