from random import randint
import tkinter as tk
from PIL import Image, ImageTk 
# Image to load image and ImageTk to place image on tkinter widget
import sys
import os

MOVE_INCREMENT = 20
# Pixels moved per tick
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second
# // gives floor value

class Snake(tk.Canvas): 
# We're going to create our snake class and inherit from the Canvas class
	def __init__(self):
		super().__init__(width=600, height=620, background='black', highlightthickness=0) 
		# Initialise dimensions, colour and border

		self.snake_positions = [(100, 100), (80, 100), (60, 100)] 
		# Initial snake block positions. Each piece will be 20 pixels apart because our pngs are 20x20
		self.food_position = self.set_new_food_position()
		# Initial food block position
		self.score = 0
		# Inital score 
		self.direction = "Right"
		self.bind_all("<Key>", self.on_key_press) # Whenever any key is pressed, we run on_key_press

		self.load_assets() 
		# Load in our assets using our method
		self.create_objects() 
		# Place our assets into our window using our method

		self.after(GAME_SPEED, self.perform_actions)
		# Call perform_actions after GAME_SPEED ms

	def load_assets(self):
		try:
			self.snake_body_image = Image.open("./4snake.png") 
			# Opens snake.png
			self.snake_body = ImageTk.PhotoImage(self.snake_body_image) 
			# Creates a photo image using the ImageTk class
			self.food_image = Image.open("./4food.png") 
			# Opens food.png
			self.food_image = ImageTk.PhotoImage(self.food_image) 
			# Creates a photo image using the ImageTk class
			self.background_image = Image.open("./1background.png")
			self.background_image = ImageTk.PhotoImage(self.background_image)

		except IOError as error: 
		# In case images cannot be found
			print(error)
			root.destroy() 
			# Closes the window from an unrecoverable error

	def create_objects(self):
		self.create_image(300, 311, image = self.background_image, tag = "background") 
		self.create_text(
			40, 16, text = f"Score {self.score}",
			tag = "score", fill = "#000000", font = ("Impact", 14))
		# Creates text, method inheritted from parent class
		for x_position, y_position in self.snake_positions: 
		# For the x and y positions we have
			self.create_image(x_position, y_position, image = self.snake_body, tag = "snake") 
			# create_image inheritted, will create our image asset and place it. A Tag makes it easy to find on the canvas
		self.create_image(*self.food_position, image = self.food_image, tags="food")
		# self.food_position[0], self.food_position[1] is replaced with *self.food_position. This destructs the tuple and passes
		# it as seperate arguments
		self.create_rectangle(8, 28, 592, 612, outline = "#525d69")
		self.create_rectangle(9, 29, 591, 611, outline = "#525d69")
		self.create_rectangle(7, 27, 593, 613, outline = "#525d69")
		# Inheritted method that creates a rectange from 7, 27 to 593,613. Top left to bottom right

	def move_snake(self):
		head_x_position, head_y_position = self.snake_positions[0]
		# Destructures out first tuple in our snake position list into 2 variables

		if self.direction == "Left":
			new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
		elif self.direction == "Right":
			new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
		elif self.direction == "Down":
			new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
		elif self.direction == "Up":
			new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)
		# Changes direction of snake depending on what self.direction is

		self.snake_positions = [new_head_position] + self.snake_positions[:-1]
		# Adds our new head position to our original snake and cuts off last block with list slicing to mimic movement

		for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
			self.coords(segment, position)
		# Zip function pairs each block tagged snake with each new snake position. Coords function moves each segment to
		# it's respective new position.

	def perform_actions(self):
		if self.check_collisions():
			python = sys.executable
			os.execl(python, python, * sys.argv)
			return
		# When collision is detected, perform actions is ended early so snake no longer moves
		self.check_food_collisions()
		self.move_snake()
		self.after(GAME_SPEED, self.perform_actions)
		# Move our snake, wait and calls this function again. Note: no () because we don't want it to return None

	def check_collisions(self):
		head_x_position, head_y_position = self.snake_positions[0]

		return (
			head_x_position in (0, 600)
			or head_y_position in (20, 620)
			or (head_x_position, head_y_position) in self.snake_positions[1:])
		# Return True if hits x border, y border or the snake itself

	def on_key_press(self, e):
		new_direction = e.keysym 
		# Checks what key was pressed during event e
		all_directions = ("Up", "Down", "Left", "Right")
		opposites = ({"Up", "Down"}, {"Left", "Right"})
		# A tuple of pairs of directions that are opposite. Dictionaries also don't care about order. up down = down up

		if (new_direction in all_directions 
			and {new_direction, self.direction} not in opposites):
		# If the direction is one of the options and the new direction is not opposite to current then execute next line
			self.direction = new_direction

	def check_food_collisions(self):
		if self.snake_positions[0] == self.food_position:
		# Checking if head position is same as food position
			self.score += 1
			self.snake_positions.append(self.snake_positions[-1])
			# Appends an extra body on top of last body piece. So when it normally would get deleted, this time
			# because it ate a food, a copy will attach on. This mimics the growth of our snake by one block

			if self.score % 5 == 0:
				global moves_per_second
				moves_per_second += 1

			self.create_image(
				*self.snake_positions[-1], image = self.snake_body, tag = "snake")
			# Creates image again to make our changes before movement. Tagged snake so it joins with our existing
			# snake blocks

			self.food_position = self.set_new_food_position()
			self.coords(self.find_withtag("food"), *self.food_position)
			# Sets a new food position and then coords moves the the png with tag food to the new position

			score = self.find_withtag("score")
			self.itemconfigure(score, text = f"Score: {self.score}", tag = "score")
			# Finds and assigns our text via it's tag. Then configures it to display our new score and re tag it as score.

	def set_new_food_position(self):
		while True:
			x_position = randint(1, 29) * MOVE_INCREMENT
			# X value randomised in 20 pixel intervals to edge (-1 because the co ordinates are for top left of an image)
			y_position = randint(3, 30) * MOVE_INCREMENT
			# Y value randomised in 20 pixel intervals to edge excluding our score section
			food_position = (x_position, y_position)

			if food_position not in self.snake_positions:
				return food_position

root = tk.Tk() 
# Creates application window
root.title("Snake") 
# Gives application a title
root.resizable(False, False) 
# Makes the window unresizable in both the x and y directions

board = Snake()
# Creates an instance of our Snake class
board.pack() 
# Puts the canvas on the window

root.mainloop() 
# Runs the application