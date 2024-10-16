import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = 10
GROUND_HEIGHT = 20

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.velocity_y = 0
        self.on_ground = False

    def update(self, ground):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check for collision with ground
        if pygame.sprite.collide_rect(self, ground):
            if self.velocity_y > 0:  # Ensure the player is falling
                self.rect.bottom = ground.rect.top
                self.on_ground = True
                self.velocity_y = 0
        else:
            self.on_ground = False

        # Check for screen boundaries
        if self.rect.x < 0:
            self.rect.x = 0  # Left boundary
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width  # Right boundary

    def jump(self):
        if self.on_ground:
            self.velocity_y -= JUMP_STRENGTH

# Ground class (green bar)
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Mario Game")

# Create a player and ground instance
player = Player()
ground = Ground()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ground)

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
    if keys[pygame.K_SPACE]:
        player.jump()

    # Update
    player.update(ground)  # Pass the ground to the player's update method

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()
    clock.tick(60)
