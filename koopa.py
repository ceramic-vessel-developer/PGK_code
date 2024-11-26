import pygame

class Koopa(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		img_path = 'assets/power_up/pngegg.png'
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = self.image.get_rect(topleft = pos)

		# movement
		self.direction = pygame.math.Vector2(1, 0)
		self.speed = 2
		self.jump_move = -16

		# status
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

	# update object position due to world scroll
	def update(self, x_shift):
		self.rect.x += x_shift