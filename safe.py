import pygame

class Zone:
    def __init__(self, y_cor, interval):
        self.y_cor = y_cor
        self.interval = interval
        self.safe_time = None
        self.time_in_safe_zone = 0

    def life_check(self, gunman, lives):
        if gunman.y >= self.y_cor-5:
            if self.safe_time is None:
                self.safe_time = pygame.time.get_ticks()
                self.time_in_safe_zone = 0
            else:
                self.time_in_safe_zone = pygame.time.get_ticks() - self.safe_time
                if self.time_in_safe_zone >= self.interval:
                    lives -= 1
                    self.safe_time = pygame.time.get_ticks()
                    if lives <= 0:
                        return lives, True
        else:
            self.safe_time = None
            self.time_in_safe_zone = 0
        return lives, False

    def get_time_in_safe_zone(self):
        return self.time_in_safe_zone
    def get_warning_message(self):
        if self.time_in_safe_zone > 0:
            return True


