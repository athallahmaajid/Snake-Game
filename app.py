import tkinter as tk
from tkinter import ttk
# from Frame import Menu
from Frame import Board

class Main(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)

        self.title('Snake Game')
        self.resizable(False, False)


        board_frame = Board(self)
        board_frame.pack()

master = Main()

if __name__ == '__main__':
    master.mainloop()
