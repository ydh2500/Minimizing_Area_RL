import pygame
import sys
pygame.init()

side = 10

class snake():
	"""docstring for snake"""
	def __init__(self, pos, color=(255,255,255)):
		self.pos = pos
		self.length = 4
		self.color = color
		self.face = "up"
		self.bodyParts = []
		for i in range(self.length):
			self.bodyParts.append(BodyParts([self.pos[0], self.pos[1] + i]))

	def moveSnake(self):
		for i in range(self.length-1, 0, -1):
			self.bodyParts[i-1].duplicate(self.bodyParts[i])
		
		if self.face == 'up':
			self.bodyParts[0].move(0, -1)
			self.pos[1] -= 1
		elif self.face == 'down':
			self.bodyParts[0].move(0, 1)
			self.pos[1] += 1
		elif self.face == 'right':
			self.bodyParts[0].move(1, 0)
			self.pos[0] += 1
		elif self.face == 'left':
			self.bodyParts[0].move(-1, 0)
			self.pos[0] -= 1

	def drawAll(self, screen):
		for part in self.bodyParts:
			part.draw(screen)

class BodyParts():
	def __init__(self, pos, color=(255,255,255)):
		self.pos = pos
		self.color = color
		
	def duplicate(self, body2):
		body2.pos = self.pos
		body2.color = self. color

	def move(self, x, y):
		self.pos[0] += x
		self.pos[1] += y		

	def draw(self, screen):
		screen.fill((self.color, pygame.Rect((self.pos[0] + 1)*side, (self.pos[1] +1)*side, side-2, side-2)))	

class Food():
	"""docstring for Food"""
	def __init__(self, pos, type):
		self.pos = pos
		self.type = type

	def keyBoardDetect():
		keyPressed = pygame.key.get_pressed()
		if keyPressed[pygame.K_LEFT]:
			self.face = 'left'
		elif keyPressed[pygame.K_RIGHT]:
			self.face = 'right'
		elif keyPressed[pygame.K_UP]:
			self.face = 'up'
		elif keyPressed[pygame.K_DOWN]:
			self.face = 'down'

		
game_screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()
counter = 0

while True:
	game_screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			keyBoardDetect()

	if counter == 10:
		Boby.moveSnake()
		counter == 0
	else :
		counter += 1
	Boby.drawAll(game_screen)
	pygame.display.flip()
	clock.tick(20)