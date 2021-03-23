import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
from tkinter import messagebox
from random import randint
from Frame import Menu
from Frame import Board

MOVE_INCREMENT = 20
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second

pygame.mixer.init()
def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

class Main(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.menu_frame = Menu(self, lambda:self.switch(self.board_frame))
        self.menu_frame.pack()

        self.board_frame = Board(self, lambda:self.switch(self.menu_frame))

        self.switch(self.menu_frame)
    def switch(self, container):
        if container == self.menu_frame:
            self.board_frame.destroy()
            self.menu_frame.pack()
        else:
            self.board_frame = Board(self, lambda:self.switch(self.menu_frame))
            self.menu_frame.pack_forget()
            self.board_frame.pack()

master = Main()

if __name__ == '__main__':
    master.mainloop()
