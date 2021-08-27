from tkinter import *
from tkinter import ttk
import json
from sys import platform
from dataclasses import dataclass
from typing import Callable, List

TESTING_FULLSCREEN = False
#TESTING_FULLSCREEN = True

FONT_FACE = "ChicagoFLF"
SCALE = 1
BASE_FONTSIZE_M = 30
BASE_FONTSIZE_L = 50
FONT_M = (FONT_FACE, int(BASE_FONTSIZE_M * SCALE))
FONT_L = (FONT_FACE, int(BASE_FONTSIZE_L * SCALE))

IPLEX_WHITE = "#ffffff"
IPLEX_YELLOW = "#e5a00d"
IPLEX_DARKGRAY = "#282a2d"

class iPlexApp(Tk):
    def __init__(self, *args, **kwargs):
        global FONT_M, FONT_L, SCALE
        Tk.__init__(self, *args, **kwargs)
        if(not TESTING_FULLSCREEN and platform == "win32"):
            self.geometry("320x240")
            SCALE = 0.3
        else:
            self.attributes('-fullscreen', True)
            SCALE = self.winfo_screenheight() / 930

        FONT_M = (FONT_FACE, int(BASE_FONTSIZE_M * SCALE))
        FONT_L = (FONT_FACE, int(BASE_FONTSIZE_L * SCALE))
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frame = ListPage(container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()

@dataclass
class MenuItem:
    label: str
    callback: Callable[[], None]
    is_submenu: bool = False

class ListPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg=IPLEX_DARKGRAY)

        # Header
        header_container = Canvas(self, bg=IPLEX_DARKGRAY, highlightthickness=0, relief="ridge")
        header_container.grid(sticky="we")
        self.header_label = Label(header_container, text="iPlex", font=FONT_L, background=IPLEX_DARKGRAY, foreground=IPLEX_YELLOW)
        self.header_label.grid(sticky="we", column=1, row=0, padx=(0, 8))
        self.left_label = Label(header_container, text=">", font=FONT_L, background=IPLEX_DARKGRAY, foreground=IPLEX_YELLOW)
        self.left_label.grid(sticky="w", column=0, row=0)
        self.right_label = Label(header_container, text="<", font=FONT_L, background=IPLEX_DARKGRAY, foreground=IPLEX_WHITE)
        self.right_label.grid(sticky="e", column=2, row=0)
        header_container.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        divider = Canvas(self)
        divider.configure(bg=IPLEX_YELLOW, height=1, bd=0, highlightthickness=0, relief="ridge")
        divider.grid(row=1, column=0, stick="we")

        # Content

        content_container = Canvas(self, bg=IPLEX_DARKGRAY, highlightthickness=0, relief="ridge")
        content_container.grid(row=2, column=0, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        self.list_container = Canvas(content_container)
        self.list_container.configure(bg=IPLEX_DARKGRAY, bd=0, highlightthickness=0)
        self.list_container.grid(row=0, column=0, sticky="nsew")
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)

        self.list_items: List[MenuItem] = []
        self.selected_index=0
        self.refresh_listdisplay()

    def get_index(self):
        return self.selected_index

    def set_index(self, ind):
        self.selected_index = ind
        self.refresh_listdisplay()

    def set_list(self, items):
        self.list_items = items
        self.refresh_listdisplay()

    def refresh_listdisplay(self):
        self.list_container.grid_forget()
        self.list_container.grid(row=0, column=0, sticky="nsew")
        for idx, item in enumerate(self.list_items):
            background = IPLEX_DARKGRAY if idx != self.selected_index else IPLEX_YELLOW
            foreground = IPLEX_DARKGRAY if idx == self.selected_index else IPLEX_YELLOW
            item_label = Label(self.list_container, text = item.label, anchor="w", font=FONT_L, background=background, foreground=foreground)
            item_arrow = Label(self.list_container, text = ">", anchor="e", font=FONT_L, background=background, foreground=foreground if item.is_submenu else background)
            item_label.grid(row=idx, column=0, sticky="ew")
            item_arrow.grid(row=idx, column=1, sticky="nsew")

        self.list_container.grid_columnconfigure(0, weight=1)

    def select_item(self):
        self.list_items[self.selected_index].callback()

def onKeyPress(event):
    c = event.keycode
    global root
    if(c == 38): #Up
        i = root.frame.get_index()
        if(i > 0):
            root.frame.set_index(i - 1)
    elif(c == 40): #Down
        i = root.frame.get_index()
        if(i < len(root.frame.list_items) - 1):
            root.frame.set_index(i + 1)
    elif(c == 37): #Left
        return
    elif(c == 39): #Right
        return
    elif(c == 104): #Menu
        return
    elif(c == 98): #Play/Pause
        return
    elif(c == 100): #Prev
        return
    elif(c == 102): #Next
        return
    elif(c == 101): #Select
        root.frame.select_item()
    else:
        print("Unrecognized:",c)

root = iPlexApp()
root.title("iPlex")
root.frame.set_list([
    MenuItem("Music", lambda:print("Chose Music"), True),
    MenuItem("Photos", lambda:print("Chose Photos"), True),
    MenuItem("Videos", lambda:print("Chose Videos"), True),
    MenuItem("Extras", lambda:print("Chose Extras"), True),
    MenuItem("Settings", lambda:print("Chose Settings"), True),
    MenuItem("Shuffle Songs", lambda:print("Chose Shuffle"), False),
    ])
root.bind('<KeyPress>', onKeyPress)
root.mainloop()