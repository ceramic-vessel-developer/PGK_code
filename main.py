import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 2000  # The total width of the map
GRAVITY = 0.5
JUMP_STRENGTH = 10
GROUND_HEIGHT = 20
LIFE_COUNTER = 3
GAP_WIDTH = 150  # Width of the gap in the ground

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2  # Start player in the center of the screen
        self.rect.y = SCREEN_HEIGHT - 150
        self.velocity_y = 0
        self.on_ground = False
        self.map_x = 100  # The player's position in the larger map (not just the screen)

    def update(self, ground_left, ground_right):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check for collision with left and right ground parts
        if pygame.sprite.collide_rect(self, ground_left) or pygame.sprite.collide_rect(self, ground_right):
            if self.velocity_y > 0:  # Ensure the player is falling
                self.rect.bottom = ground_left.rect.top  # Align with the top of the ground
                self.on_ground = True
                self.velocity_y = 0
        else:
            self.on_ground = False

        # Update the player's position in the larger map
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >= 5:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.x <= SCREEN_WIDTH - 55:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:  # Allow jumping only when on the ground
            self.velocity_y -= JUMP_STRENGTH

        # Update map position based on the player's position
        self.map_x = self.rect.x

# Ground class (green bar with two sections to form a gap)
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, width):
        super().__init__()
        self.image = pygame.Surface((width, GROUND_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT

# Game over function
def game_over(screen):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 55)
    text = font.render('Game Over', True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Display for 3 seconds
    pygame.quit()
    sys.exit()

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Mario Game with Fixed Player and Lives")

# Create ground sections (split by the gap)
ground_left = Ground(0, (MAP_WIDTH - GAP_WIDTH) // 2)  # Left side of the gap
ground_right = Ground((MAP_WIDTH + GAP_WIDTH) // 2, (MAP_WIDTH - GAP_WIDTH) // 2)  # Right side of the gap

# Create player instance
player = Player()

# Life counter
life_counter = LIFE_COUNTER

# Font for life counter
font = pygame.font.SysFont(None, 35)

# Camera offset (how far the map is scrolled horizontally)
camera_x = 0

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player input and movement
    player.update(ground_left, ground_right)

    # Adjust camera position based on player's position
    if player.rect.x > SCREEN_WIDTH // 2 and player.rect.x < MAP_WIDTH - SCREEN_WIDTH // 2:
        camera_x = player.rect.x - SCREEN_WIDTH // 2  # Center player on screen when they are in the middle of the map
    elif player.rect.x <= SCREEN_WIDTH // 2:  # Allow player to go left until screen edge
        camera_x = 0
    elif player.rect.x >= MAP_WIDTH - SCREEN_WIDTH // 2:  # Allow player to go right until screen edge
        camera_x = MAP_WIDTH - SCREEN_WIDTH

    # Check if player falls through the gap
    if not pygame.sprite.collide_rect(player, ground_left) and not pygame.sprite.collide_rect(player, ground_right) and player.rect.y >= SCREEN_HEIGHT:
        life_counter -= 1
        if life_counter < 0:
            game_over(screen)  # End the game if life counter is negative
        else:
            player.rect.x, player.rect.y = SCREEN_WIDTH // 2 - player.rect.width // 2, SCREEN_HEIGHT - 150  # Reset player position

    # Update display
    screen.fill(WHITE)

    # Shift the ground sections according to the camera position
    ground_left.rect.x = 0 - camera_x - SCREEN_WIDTH//2 + 50
    ground_right.rect.x = (MAP_WIDTH + GAP_WIDTH) // 2 - camera_x - SCREEN_WIDTH//2

    # Create a sprite group and add all elements to draw
    all_sprites = pygame.sprite.Group(player, ground_left, ground_right)
    all_sprites.draw(screen)

    # Draw life counter
    life_text = font.render(f"Lives: {life_counter}", True, BLACK)
    screen.blit(life_text, (10, 10))

    # Refresh the display
    pygame.display.flip()
    clock.tick(60)
