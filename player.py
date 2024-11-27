import pygame

from settings import tile_size
from support import import_sprite
from tile import Tile


class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		# self._import_character_assets()
		# self.frame_index = 0
		# self.animation_speed = 0.15
		self.size = (35, 50)
		img_path = 'assets/player/mario.png'
		self.refresh_image(img_path)
		self.building = False
		self.built = False
		# self.image = pygame.image.load(img_path)
		self.rect = self.image.get_rect(topleft = pos)
		self.mask = pygame.mask.from_surface(self.image)

		self.pos = list(pos)

		# player movement
		self.direction = pygame.math.Vector2(0, 0)
		self.speed = 5
		self.jump_move = -16

		# player status
		self.life = 5
		self.score = 20
		self.super_mario = False
		self.game_over = False
		self.win = False
		self.status = "idle"
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

	def refresh_image(self, path):
		img_path = path
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
	# gets all the image needed for animating specific player action
	# def _import_character_assets(self):
	# 	character_path = "assets/player/"
	# 	self.animations = {
	# 		"idle": [],
	# 		"walk": [],
	# 		"jump": [],
	# 		"fall": [],
	# 		"lose": [],
	# 		"win": []
	# 	}
	# 	for animation in self.animations.keys():
	# 		full_path = character_path + animation
	# 		self.animations[animation] = import_sprite(full_path)
	#
	# # animates the player actions
	def _animate(self):
		# animation = self.animations[self.status]
		#
		# # loop over frame index
		# self.frame_index += self.animation_speed
		# if self.frame_index >= len(animation):
		# 	self.frame_index = 0
		# image = animation[int(self.frame_index)]
		# image = pygame.transform.scale(image, self.size)
		# if self.facing_right:
		# 	self.image = image
		# else:
		# 	flipped_image = pygame.transform.flip(image, True, False)
		# 	self.image = flipped_image

		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	# checks if the player is moving towards left or right or not moving
	def _get_input(self, player_event, tiles, blocks):
		if player_event != False:
			if player_event == "right":
				self.direction.x = 1
				self.facing_right = True
			elif player_event == "left":
				self.direction.x = -1
				self.facing_right = False
		else:
			self.direction.x = 0

		if player_event != False and self.building and self.on_ground and not self.built:
			if player_event == "build_up":
				self._build_tile((self.rect.x,self.rect.y - tile_size), tiles,blocks)
			elif player_event == "build_left":
				self._build_tile((self.rect.x - tile_size,self.rect.y ), tiles,blocks)
			elif player_event == "build_down":
				self._build_tile((self.rect.x,self.rect.y), tiles, blocks,True)
			elif player_event == "build_right":
				self._build_tile((self.rect.x + tile_size,self.rect.y), tiles,blocks)

		if not player_event:
			self.built = False

	def _jump(self):
		self.direction.y = self.jump_move

	def _build_tile(self, pos, tiles,blocks, under=False):
		if self.score >= 10 and self.on_ground:

			tile = Tile(pos=pos, size=tile_size)
			if not under:
				temp = pygame.sprite.GroupSingle()
				temp.add(tile)

				for sprite in tiles.sprites():
					if sprite.rect.colliderect(tile.rect):
						print("Nie")
						del tile
						return

				del temp
				tiles.add(tile)
			else:
				temp_y = self.rect.y

				self.rect.y -= tile_size

				for sprite in tiles.sprites():
					if sprite.rect.colliderect(self.rect):
						self.rect.y = temp_y
						print("Nie down")
						return
				for sprite in blocks.sprites():
					if sprite.rect.colliderect(self.rect):
						self.rect.y = temp_y
						print("Nie nie down bloki")
						return

				tile = Tile(pos=pos, size=tile_size)
				tiles.add(tile)
			self.built = True
			self.score -= 10




	# identifies player action
	def _get_status(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 1:
			self.status = "fall"
		elif self.direction.x != 0:
			self.status = "walk"
		else:
			self.status = "idle"

	def _handle_size_change(self):
		if self.super_mario:
			self.size = (42, 60)
		else:
			self.size = (35, 50)

		self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))

	def eat_mushroom(self):
		self.super_mario = True
		self._handle_size_change()

	def hit(self):
		if self.super_mario:
			self.super_mario = False
			self._handle_size_change()
		else:
			self.life -= 1

	def handle_build(self):
		self.building = True
		self.refresh_image("assets/player/mario_bud.png")

	def handle_build_disable(self):
		self.building = False
		self.refresh_image("assets/player/mario.png")

	# update the player's state
	def update(self, player_event,tiles,blocks):
		self._get_status()
		if self.life > 0 and not self.game_over:
			if player_event == "space" and self.on_ground and not self.building:
				self._jump()
			elif player_event == "build":
				self.handle_build()
			elif player_event == "build_disable":
				self.handle_build_disable()
			else:
				self._get_input(player_event,tiles,blocks)
		elif self.game_over and self.win:
			self.direction.x = 0
			self.status = "win"
		else:
			self.direction.x = 0
			self.status = "lose"
		self._animate()
