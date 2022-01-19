import pygame
from lasers import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 7
        self.ready = True
        self.timer = 0
        self.cooldown = 500

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys [pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys [pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys [pygame.K_SPACE] and self.ready: 
            self.shoot()
            self.ready = False
            self.timer = pygame.time.get_ticks()

    def escape(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x + 60 >= 600:
            self.rect.x = 540

    def shoot(self):
        self.lasers.add(Laser(self.rect.center, 8, self.rect.bottom))

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.timer >= self.cooldown:
                self.ready = True

    def update(self):
        self.get_input()
        self.escape()
        self.recharge()
        self.lasers.update()