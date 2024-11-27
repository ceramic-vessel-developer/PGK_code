import pygame, sys
from settings import *
from world import World

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

class Platformer:
	def __init__(self, screen, width, height):
		self.screen = screen
		self.clock = pygame.time.Clock()
		self.player_event = False

		self.bg_img = pygame.image.load('assets/terrain/bg.jpg')
		self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

	def main(self):
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


if __name__ == "__main__":
	play = Platformer(screen, WIDTH, HEIGHT)
	play.main()