import pygame

from power_up import PowerUp
from settings import tile_size


class LuckyBlock(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = list(pos)
        self.active = True
        self.size = size
        self.refresh_image()

    # update object position due to world scroll
    def update(self, x_shift):
        self.rect.x += x_shift
        self.pos[0] += x_shift

    def refresh_image(self):
        img_path = 'assets/terrain/lucky_block.png' if self.active else 'assets/terrain/empty_block.png'
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=self.pos)

    def hit(self, power_ups):
        if self.active:
            self.active = False
            power_up_sprite = PowerUp((self.pos[0], self.pos[1]-tile_size), tile_size)
            power_ups.add(power_up_sprite)
            self.refresh_image()

