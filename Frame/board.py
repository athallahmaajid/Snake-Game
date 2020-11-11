import tkinter as tk
from PIL import Image, ImageTk
import pygame
from tkinter import messagebox
from random import randint

MOVE_INCREMENT = 20
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second

pygame.mixer.init()
def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

class Board(tk.Canvas):
    def __init__(self, container, show_menu):
        super().__init__(width=600, height=620, background='black', highlightthickness=0)

        self.show_menu = show_menu

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food()
        self.score = 0
        self.direction = 'Right'
        self.container = container

        self.bind_all('<Key>', self.on_key_pressed)
        self.load_assets()
        self.create_object()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open('snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('food.png')
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError:
            messagebox.showerror('ERROR', 'Aplikasi mendeteksi adanya kesalahan')
            self.container.destroy()
    
    def create_object(self):
        self.create_text(100, 12, text=f'Score: {self.score} Speed: {moves_per_second}', tag='score', fill='#fff', font=('Times New Roman', 14))
        for x, y in self.snake_positions:
            self.create_image(x, y, image=self.snake_body, tag='snake')
        
        self.create_image(self.food_position[0], self.food_position[1], image=self.food,  tag='food')
        self.create_rectangle(7, 27, 593, 613, outline='#525d69')

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        if self.direction == 'Right':
            new_head_position = (head_x_position+MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Left':
            new_head_position = (head_x_position-MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Up':
            new_head_position = (head_x_position, head_y_position-MOVE_INCREMENT)
        elif self.direction == 'Down':
            new_head_position = (head_x_position, head_y_position+MOVE_INCREMENT)
        else:
            new_head_position = self.snake_positions
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)
    
    def perform_actions(self):
        if self.check_collision():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)
    
    def check_collision(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (
            head_x_position in (0, 600) or
            head_y_position in (20, 620) or
            (head_x_position, head_y_position) in self.snake_positions[1:]
        )
    def on_key_pressed(self, e):
        new_direction = e.keysym
        all_directions = ['Up', 'Down', 'Right', 'Left']
        opposites = ({'Up', 'Down'}, {'Right', 'Left'})

        if (new_direction in all_directions and {new_direction, self.direction} not in opposites):
            self.direction = new_direction

    def check_food_collision(self):
        global moves_per_second
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            if (self.score % 5) == 0:
                moves_per_second += 1
            self.snake_positions.append(self.snake_positions[-1])
            
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')

            self.food_position = self.set_new_food()
            self.coords(self.find_withtag('food'), self.food_position)

            score = self.find_withtag('score')
            self.itemconfigure(score, text=f'Score: {self.score} Speed: {moves_per_second}', tag='score')

    def set_new_food(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        play_sound('super-mario-death-sound-sound-effect.mp3')
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, text=f'Game Over, you are scored {self.score}', fill='#fff', font=('FreeMono', 20))
        
        retry_button = tk.Button(self, text='Retry', bg='black', fg='white', width=15, command=self.retry)
        retry_button.place(x=self.winfo_width()/2-225, y=self.winfo_height()/2+40)

        back_button = tk.Button(self, text='Back', bg='black', fg='white', width=15, command=self.show_menu)
        back_button.place(x=self.winfo_width()/2-75, y=self.winfo_height()/2+40)
        
        quit_button = tk.Button(self, text='Quit', bg='black', fg='white', width=15, command=lambda:self.container.destroy())
        quit_button.place(x=self.winfo_width()/2+75, y=self.winfo_height()/2+40)
    
    def retry(self):
        self.pack_forget()
        board_frame = Board(self.container, lambda:self.show_menu)
        self.container.switch(self.container.board_frame)