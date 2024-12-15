import pygame
from settings import HEIGHT, WIDTH

pygame.font.init()

class Game:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.Font("assets/fonts/mario2.ttf", 30)
		self.message_color = pygame.Color("white")
		self.displays_screen = False

	# death screen
	def _game_death(self,player):
		"""Draw the death screen showing remaining lives and current world."""
		WHITE = (255, 255, 255)
		BLACK = (0, 0, 0)
		RED = (255, 0, 0)

		# TITLE_FONT = pygame.font.Font(pygame.font.match_font('impact'), 80)
		SUBTITLE_FONT = pygame.font.Font("assets/fonts/mario2.ttf", 30)
		INFO_FONT = pygame.font.Font("assets/fonts/mario2.ttf", 30)
		# Fill the screen with black
		self.screen.fill(BLACK)

		# Show remaining lives
		lives_text = SUBTITLE_FONT.render(f"lives      {player.life}", True, WHITE)
		lives_rect = lives_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
		self.screen.blit(lives_text, lives_rect)

		# Show current world
		world_text = INFO_FONT.render(f"world    1", True, WHITE)
		world_rect = world_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
		self.screen.blit(world_text, world_rect)
		self.displays_screen = True

	# if player ran out of life or fell below the platform
	def _game_lose(self, player):
		player.game_over = True
		message = self.font.render('you lose...', True, self.message_color)
		self.screen.blit(message,(WIDTH // 3 + 70, 70))

	# if player reach the goal
	def _game_win(self, player):
		player.game_over = True
		player.win = True
		message = self.font.render('You Win!!', True, self.message_color)
		self.screen.blit(message,(WIDTH // 3, 70))

	# checks if the game is over or not, and if win or lose
	def game_state(self, player, goal):
		x, y, w, h = goal.rect
		if player.life <= 0 or player.rect.y >= HEIGHT:
			self._game_lose(player)
		elif player.rect.colliderect(goal.rect):
			if player.status != "win":
				if player.rect.clipline((x,y),(x+w,y)):
					player.score += 100
				elif player.rect.clipline((x,y- h//3),(x+w,y-h//3)):
					player.score += 50
				else:
					player.score += 20

			self._game_win(player)
		elif player.is_hit:
			if self.displays_screen:
				pygame.time.wait(2000)
				player.is_hit = not player.is_hit
				self.displays_screen = False
			self._game_death(player)

		else:
			None

	def show_life(self, player):
		life_size = 30
		img_path = "assets/life/life.png"
		life_image = pygame.image.load(img_path)
		life_image = pygame.transform.scale(life_image, (life_size, life_size))
		# life_rect = life_image.get_rect(topleft = pos)
		indent = 0
		for life in range(player.life):
			indent += life_size
			self.screen.blit(life_image, (indent, life_size))
	
	def show_score(self, player):
		message = self.font.render(str(player.score), True, self.message_color)
		self.screen.blit(message,(WIDTH - WIDTH // 7, 0))