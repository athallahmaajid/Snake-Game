import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
MOVE_PER_SECOND = 15
GAME_SPEED = 1000 // MOVE_PER_SECOND

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background='black', highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food()
        self.score = 0
        self.direction = 'Right'

        self.bind_all('<Key>', self.on_key_pressed)
        self.load_assets()
        self.create_object()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open('./assets/snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('./assets/food.png')
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError:
            messagebox.showerror('ERROR', 'Aplikasi mendeteksi adanya kesalahan')
            master.destroy()
    
    def create_object(self):
        self.create_text(45, 12, text=f'Score: {self.score}', tag='score', fill='#fff', font=('Times New Roman', 14))
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
            pass
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]
        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)
    
    def perform_actions(self):
        if self.check_collision():
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
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')

            self.food_position = self.set_new_food()
            self.coords(self.find_withtag('food'), self.food_position)

            score = self.find_withtag('score')
            self.itemconfigure(score, text=f'Score: {self.score}', tag='score')

    def set_new_food(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

master = tk.Tk()
master.title('Snake Game')
master.resizable(False, False)

board = Snake()
board.pack()

if __name__ == '__main__':
    master.mainloop()
