import pygame

class Koopa(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		img_path = 'assets/koopa/koopa.png'
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = list(pos)
		self.size = size

		# movement
		self.direction = pygame.math.Vector2(1, 0)
		self.speed = 2
		self.jump_move = -16
		self.stage = 0

		# status
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

	# update object position due to world scroll
	def update(self, x_shift):
		self.rect.x += x_shift

	def refresh_image(self, path):
		img_path = path
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.scale(self.image, (self.size, self.size))

	def hit(self):
		if self.stage == 0:
			self.refresh_image("assets/koopa/koopa_shell.png")
			self.speed = 0
			self.stage +=1
		elif self.stage == 1:
			self.speed = 3
			self.stage +=1
		elif self.stage == 2:
			self.speed = 0
			self.stage -=1

