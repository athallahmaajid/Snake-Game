import tkinter as tk
from tkinter import ttk

class Menu(tk.Frame):
    def __init__(self, container, show_board, **kwargs):
        super().__init__(container, **kwargs)

        self['bg'] = 'black'

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        game_title = tk.Label(self, text='Snake Game', bg='black', fg='white', font=('FreeMono', 44))
        game_title.grid(row=0, column=0, padx=180, pady=120)

        switch_button = tk.Button(self, text='Play', bg='black', fg='white', width=10, font=('FreeMono', 44), command=show_board)
        switch_button.grid(row=1, column=0, padx=160, pady=120)
        switch_button.columnconfigure(0, weight=1)
