import pygame

class Goomba(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		img_path = 'assets/goomba/goomba.png'
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = self.image.get_rect(topleft = pos)
		self.size = size
		self.pos = pos

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
		self.killed = False
		self.killed_counter = 60

	# update object position due to world scroll
	def update(self, x_shift):
		self.rect.x += x_shift
		if self.killed:
			if self.killed_counter <= 0:
				self.kill()
			else:
				self.killed_counter -= 1


	def hit(self):
		self.killed = True
		self.image = pygame.transform.scale(self.image, (self.size, self.size*0.35))
		self.rect.topleft = (self.rect.topleft[0],self.rect.topleft[1]+self.size*0.65)