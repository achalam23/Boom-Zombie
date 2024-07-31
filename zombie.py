import pygame
import random

class Zombie:
    def __init__(self):
        self.img = pygame.image.load('zombie.png')
        self.rect = self.img.get_rect()
        self.rect.x = random.randint(0, 768)
        self.rect.y = random.randint(0, 568)
        self.x_speed = random.choice([2, -2])
        self.y_speed = random.choice([2, -2])

    def update(self):
        self.rect.x += self.x_speed
        if self.rect.x <= 0:
            self.rect.x = 0
            self.x_speed = -self.x_speed
        elif self.rect.x >= 768 - self.rect.width:
            self.rect.x = 768 - self.rect.width
            self.x_speed = -self.x_speed

        self.rect.y += self.y_speed
        if self.rect.y <= 0:
            self.rect.y = 0
            self.y_speed = -self.y_speed
        elif self.rect.y >= 568 - self.rect.height:
            self.rect.y = 568 - self.rect.height
            self.y_speed = -self.y_speed

    def display(self, screen):
        screen.blit(self.img, self.rect)

