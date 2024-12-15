from turtledemo.penrose import start

import pygame, sys
from settings import *
from world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

class Platformer:
	def __init__(self, screen, width, height):
		self.button_image = None
		self.bg_img = None
		self.screen = screen
		self.clock = pygame.time.Clock()
		self.player_event = False
		self.width = width
		self.height = height




	def main(self):
		self.start_screen()

		self.bg_img = pygame.image.load('assets/terrain/bg.jpg')
		self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))

		"""Game logic"""
		world = World(world_map, self.screen)
		while True:
			self.screen.blit(self.bg_img, (0, 0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.player_event = "left"
					if event.key == pygame.K_RIGHT:
						self.player_event = "right"
					if event.key == pygame.K_SPACE:
						self.player_event = "space"
					if event.key == pygame.K_1:
						self.player_event = "build"
					if event.key == pygame.K_0:
						self.player_event = "build_disable"
					if event.key == pygame.K_w:
						self.player_event = "build_up"
					if event.key == pygame.K_a:
						self.player_event = "build_left"
					if event.key == pygame.K_s:
						self.player_event = "build_down"
					if event.key == pygame.K_d:
						self.player_event = "build_right"
				elif event.type == pygame.KEYUP:
					self.player_event = False

			world.update(self.player_event)
			pygame.display.update()
			self.clock.tick(60)

	def draw_start_screen(self):
		"""Draw the start screen."""
		# Draw the background image
		screen.blit(self.bg_img, (0, 0))

		# Draw the start button
		screen.blit(self.button_image, (self.button_x,self.button_y))

	def start_screen(self):
		"""Handle the start screen logic."""

		self.bg_img = pygame.image.load('assets/start_screen/mario-title.png')
		self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))

		self.button_image = pygame.image.load("assets/start_screen/mario-title-button.png")  # Replace with your Play button image
		self.button_image = pygame.transform.scale(self.button_image, (400, 50))

		self.button_x = (self.width - self.button_image.get_width()) // 2
		self.button_y = (self.height - self.button_image.get_height()) // 2 + 100
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse_x, mouse_y = event.pos
					if self.button_x <= mouse_x <= self.button_x + self.button_image.get_width() and self.button_y <= mouse_y <= self.button_y + self.button_image.get_height():
						return  # Exit the start screen and start the game

			# Draw the start screen
			self.draw_start_screen()

			# Update the display
			# pygame.display.flip()
			pygame.display.update()
			self.clock.tick(60)


if __name__ == "__main__":
	play = Platformer(screen, WIDTH, HEIGHT)
	play.main()