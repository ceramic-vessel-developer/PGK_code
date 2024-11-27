import pygame

from LuckyBlock import LuckyBlock
from coin import Coin
from goomba import Goomba
from koopa import Koopa
from power_up import PowerUp
from settings import tile_size, WIDTH
from tile import Tile
from trap import Trap
from goal import Goal
from player import Player
from game import Game

class World:
	def __init__(self, world_data, screen):
		self.screen = screen
		self.world_data = world_data
		self._setup_world(world_data)
		self.world_shift = 0
		self.current_x = 0
		self.gravity = 0.7
		self.game = Game(self.screen)

	# generates the world
	def _setup_world(self, layout):
		self.tiles = pygame.sprite.Group()
		self.traps = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.coins = pygame.sprite.Group()
		self.power_ups = pygame.sprite.Group()
		self.lucky_blocks = pygame.sprite.Group()
		self.goombas = pygame.sprite.Group()
		self.koopas = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				x, y = col_index * tile_size, row_index * tile_size
				if cell == "X":
					tile = Tile((x, y), tile_size)
					self.tiles.add(tile)
				elif cell == "t":
					tile = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
					self.traps.add(tile)
				elif cell == "P":
					player_sprite = Player((x, y))
					self.player.add(player_sprite)
				elif cell == "G":
					goal_sprite = Goal((x, y), tile_size)
					self.goal.add(goal_sprite)
				elif cell == "c":
					coin_sprite = Coin((x, y), tile_size)
					self.coins.add(coin_sprite)
				elif cell == "g":
					power_up_sprite = PowerUp((x, y), tile_size)
					self.power_ups.add(power_up_sprite)
				elif cell == "L":
					lucky_block = LuckyBlock((x, y), tile_size)
					self.lucky_blocks.add(lucky_block)
				elif cell == "k":
					koopa = Koopa((x, y), tile_size*0.8)
					self.koopas.add(koopa)
				elif cell == "o":
					goomba = Goomba((x, y), tile_size*0.8)
					self.goombas.add(goomba)

	# world scroll when the player is walking towards left/right
	def _scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < WIDTH // 3 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > WIDTH - (WIDTH // 3) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 3

	# add gravity for player to fall
	def _apply_gravity(self, player, gravity = 0.0):
		if not gravity:
			gravity = self.gravity
		player.direction.y += gravity
		player.rect.y += player.direction.y

	# prevents player to pass through objects horizontally
	def _horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				# checks if moving towards right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		for sprite in self.lucky_blocks.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				# checks if moving towards right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right
		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False


	def _horizontal_npc_movement_collision(self,player):
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					player.direction *= -1
				# checks if moving towards right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					player.direction *= -1

		for sprite in self.lucky_blocks.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					player.direction *= -1
				# checks if moving towards right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					player.direction *= -1
		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	# prevents player to pass through objects vertically
	def _vertical_movement_collision(self):
		player = self.player.sprite
		self._apply_gravity(player)

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				# checks if moving towards up
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
					if player.super_mario:
						sprite.kill()

		for l_sprite in self.lucky_blocks.sprites():
			if l_sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					player.rect.bottom = l_sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				# checks if moving towards up
				elif player.direction.y < 0:
					player.rect.top = l_sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
					l_sprite.hit(self.power_ups)
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False

	def _vertical_npc_movement_collision(self,player):
		self._apply_gravity(player,12.0)

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				# checks if moving towards up
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		for sprite in self.lucky_blocks.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				# checks if moving towards up
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False

	# add consequences when player run through traps
	def _handle_traps(self):
		player = self.player.sprite

		for sprite in self.traps.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0 or player.direction.y > 0:
					player.rect.x += tile_size
				elif player.direction.x > 0 or player.direction.y > 0:
					player.rect.x -= tile_size
				player.hit()

	def _handle_coins(self):
		player = self.player.sprite

		for sprite in self.coins.sprites():
			if sprite.rect.colliderect(player.rect):
				player.score += 10
				sprite.kill()

	def _handle_power_ups(self):
		player = self.player.sprite

		for sprite in self.power_ups.sprites():
			if sprite.rect.colliderect(player.rect):
				player.eat_mushroom()
				sprite.kill()
	def _handle_shell_collision(self):
		for koopa in self.koopas.sprites():
			if koopa.stage == 2:
				for goomba in self.goombas.sprites():
					if goomba.rect.colliderect(koopa.rect):
						goomba.kill()


	def _handle_vertical_collision_with_enemies(self):
		immune = False
		player = self.player.sprite
		for sprite in self.goombas.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					# player.rect.bottom = sprite.rect.top
					# player.direction.y = 0
					# player.on_ground = True
					sprite.kill()
				# checks if moving towards up
				elif player.direction.y < 0:
					if player.direction.x <= 0 and sprite.direction.x >= 0:
						player.rect.x += tile_size
					elif player.direction.x >= 0 and sprite.direction.x <= 0:
						player.rect.x -= tile_size
					player.hit()

		for sprite in self.koopas.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					# player.rect.bottom = sprite.rect.top
					# player.direction.y = 0
					# player.on_ground = True
					sprite.hit()
					immune = True
					player._jump()
				# checks if moving towards up
				elif player.direction.y < 0:
					if player.direction.x <= 0 and sprite.direction.x >= 0:
						player.rect.x += tile_size
					elif player.direction.x >= 0 and sprite.direction.x <= 0:
						player.rect.x -= tile_size
					player.hit()
		return immune
		# if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
		# 	player.on_ground = False
		# if player.on_ceiling and player.direction.y > 0:
		# 	player.on_ceiling = False

	def _handle_horizontal_collision_with_enemies(self):
		player = self.player.sprite

		for sprite in self.goombas.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left

				if player.direction.x <= 0 and sprite.direction.x >= 0:
					player.rect.x += tile_size
				elif player.direction.x >= 0 and sprite.direction.x <= 0:
					player.rect.x -= tile_size
				player.hit()
				# if player.direction.x < 0:
				# 	player.rect.left = sprite.rect.right
				# 	player.on_left = True
				# 	self.current_x = player.rect.left
				# # checks if moving towards right
				# elif player.direction.x > 0:
				# 	player.rect.right = sprite.rect.left
				# 	player.on_right = True
				# 	self.current_x = player.rect.right

		for sprite in self.koopas.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left

				if player.direction.x <= 0 and sprite.direction.x >= 0:
					player.rect.x += tile_size
				elif player.direction.x >= 0 and sprite.direction.x <= 0:
					player.rect.x -= tile_size
				player.hit()
			# if player.direction.x < 0:
			# 	player.rect.left = sprite.rect.right
			# 	player.on_left = True
			# 	self.current_x = player.rect.left
			# # checks if moving towards right
			# elif player.direction.x > 0:
			# 	player.rect.right = sprite.rect.left
			# 	player.on_right = True
			# 	self.current_x = player.rect.right
		# if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
		# 	player.on_left = False
		# if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
		# 	player.on_right = False

	def _handle_collisions_with_enemies(self):
		immune = self._handle_vertical_collision_with_enemies()
		if immune:
			return
		self._handle_horizontal_collision_with_enemies()

	# updating the game world from all changes commited
	def update(self, player_event):
		# for tile
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.screen)

		# for trap
		self.traps.update(self.world_shift)
		self.traps.draw(self.screen)

		# for coins
		self.coins.update(self.world_shift)
		self.coins.draw(self.screen)

		# for power ups
		self.power_ups.update(self.world_shift)
		self.power_ups.draw(self.screen)

		# for goal
		self.goal.update(self.world_shift)
		self.goal.draw(self.screen)

		# for lucky blocks
		self.lucky_blocks.update(self.world_shift)
		self.lucky_blocks.draw(self.screen)

		# for koopas
		self.koopas.update(self.world_shift)
		self.koopas.draw(self.screen)

		# for goombas
		self.goombas.update(self.world_shift)
		self.goombas.draw(self.screen)


		self._scroll_x()

		# for player
		self._horizontal_movement_collision()
		self._vertical_movement_collision()
		self._handle_collisions_with_enemies()
		self._handle_traps()
		self._handle_coins()
		self._handle_power_ups()
		self._handle_shell_collision()
		self.player.update(player_event,self.tiles,self.lucky_blocks)
		self.game.show_life(self.player.sprite)
		self.game.show_score(self.player.sprite)
		self.player.draw(self.screen)

		# for npcs
		for sprite in self.power_ups.sprites():
			self._horizontal_npc_movement_collision(sprite)
			self._vertical_npc_movement_collision(sprite)
		for sprite in self.goombas.sprites():
			self._horizontal_npc_movement_collision(sprite)
			self._vertical_npc_movement_collision(sprite)
		for sprite in self.koopas.sprites():
			self._horizontal_npc_movement_collision(sprite)
			self._vertical_npc_movement_collision(sprite)

		self.game.game_state(self.player.sprite, self.goal.sprite)
