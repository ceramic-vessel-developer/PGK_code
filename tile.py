import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, size, is_floor=False):
		super().__init__()
		if is_floor:
			img_path = 'assets/terrain/floor.png'
		else:
			img_path = 'assets/terrain/brick.png'
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = self.image.get_rect(topleft = pos)

	# update object position due to world scroll
	def update(self, x_shift):
		self.rect.x += x_shift