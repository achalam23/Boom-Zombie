import pygame
import random
import math

class Health_Pack:
    def __init__(self):
        self.image = pygame.image.load('hospital.png')
        self.rect = self.image.get_rect()
        self.active = False
        self.spawn_time = None
        self.duration = 10000
        self.blink_interval = 500
        self.last_blink_time = 0
        self.visible = True

    def spawn(self):
        self.rect.x = random.randint(0, 768)
        self.rect.y = random.randint(0, 568)
        self.active = True
        self.spawn_time = pygame.time.get_ticks()
        self.last_blink_time = self.spawn_time

    def display(self, screen):
        if self.active and self.visible:
            screen.blit(self.image, self.rect)

    def health_collision(self, gunman):
        if self.active:
            distance = math.sqrt((math.pow(self.rect.x - gunman.x, 2)) + (math.pow(self.rect.y - gunman.y, 2)))
            if distance < 27:
                self.active = False
                return True
        return False

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.spawn_time
            if elapsed_time > self.duration:
                self.active = False
            elif elapsed_time > 7000:
                if current_time - self.last_blink_time >= self.blink_interval:
                    self.visible = not self.visible
                    self.last_blink_time = current_time
