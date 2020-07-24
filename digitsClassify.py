# paint on a grid

import pygame
import sklearn
import numpy as np
import pickle
import random
import math


pygame.init()

# screen settings
size = width, height = 800, 600
bg_color = 0, 0, 0
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

font = pygame.font.Font('freesansbold.ttf', 32) 

# model
filename = "mnist_model"
with open(filename, 'rb') as f:
	model = pickle.load(f)


class Canvas:
	def __init__(self):
		self.res = 28
		self.drawing = False
		self.cells = np.zeros((self.res, self.res))
		self.cell_size = int((height * .8) / self.res)
		# for i in range(400):
		# 	self.cells[random.randint(0,27)][random.randint(0,27)] = 1

	def draw(self):
		siz = self.cell_size
		for i, col in enumerate(self.cells):
			for j, cell in enumerate(col):
				if cell > 0:
					cell_col = (cell, cell, cell)
					pygame.draw.rect(screen, cell_col, (j*siz, i*siz, siz, siz))

		if self.drawing:
			# get cell that mouse is on
			m = pygame.mouse.get_pos()
			x = math.floor(m[0] / self.cell_size)
			y = math.floor(m[1] / self.cell_size)
			# turn it on	
			if x < self.res and y < self.res:
				if self.cells[y][x] < 255:
					self.cells[y][x] = 255
				
				# make brush thicker
				extra = [[-1, 0], [1, 0], [0, -1], [0, 1]]
				for c in extra:
					try:
						a, b = c[0], c[1]
						if self.cells[y+a][x+b] < 100:
							self.cells[y+a][x+b] = 100
					except: pass

		# draw border of canvas
		canvas_width = self.res * self.cell_size
		pygame.draw.line(screen, white, (0, canvas_width), (canvas_width, canvas_width), 3)
		pygame.draw.line(screen, white, (canvas_width, 0), (canvas_width, canvas_width), 3)


# button for clearing canvas
class Button:
	def __init__(self, pos, size, text):
		self.pos = pos
		self.size = size 
		self.text = text

	# return true if mouse is over the button
	def isOn(self):
		m_pos = pygame.mouse.get_pos()
		x, y = m_pos[0], m_pos[1]

		if self.pos[0] <= x <= self.pos[0] + self.size[0]:
			if self.pos[1] <=  y <= self.pos[1] + self.size[1]:
				return True
		return False

	# draw the button
	def draw(self):
		if self.isOn(): col = (200, 200, 200)
		else: col = (255, 255, 255)
		
		x, y = self.pos[0], self.pos[1]
		w, h = self.size[0], self.size[1]
		
		text = font.render(self.text, True, bg_color, col) 
		text_rect = text.get_rect() 
		text_rect.center = (x + (w // 2), y + (h // 2)) 

		pygame.draw.rect(screen, col, (x, y, w, h))
		screen.blit(text, text_rect) 

	def pressed(self, canvas):
		if self.isOn():
			canvas.cells = np.zeros((canvas.res, canvas.res))


class UI:
	def __init__(self):
		pass


def main():
	clock = pygame.time.Clock()
	run = True

	canvas = Canvas()
	canvas_width = (canvas.res * canvas.cell_size)
	reset_button_pos = ((canvas_width + (width - canvas_width)//2) - 150 , 100)
	reset_button = Button(reset_button_pos, (300, 100), "Reset Canvas")

	i = 0
	while run:
		clock.tick(60)

		i += 1
		# predict once every 60 frames
		if i == 60:
			print(model.predict(canvas.cells.reshape(1, -1)))
			# print(canvas.cells.reshape(1,-1))
			i = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				canvas.drawing = True
				reset_button.pressed(canvas)
			if event.type == pygame.MOUSEBUTTONUP:
				canvas.drawing = False

		screen.fill(bg_color)
		canvas.draw()
		reset_button.draw()

		pygame.display.flip()

	pygame.quit()
	quit()


main()

