import tkinter as tk
from tkinter import ttk

class Menu(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # game_title = tk.Label(self, text='Snake-Game: re', bg='black', fg='white')
        # game_title.grid(row=0, column=0)
        # game_title.columnconfigure(0, weight=1)

        # switch_button = tk.Button(self, text='Play', bg='black', fg='white')
        # switch_button.grid(row=1, column=0)
        # switch_button.columnconfigure(0, weight=1)

master = tk.Tk()
m = Menu(master, bg='black', width=600, height=620)
m.grid(row=0, column=0)

master.mainloop()