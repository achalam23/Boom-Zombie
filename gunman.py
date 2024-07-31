def gunmanDisplay(screen, gunmanImg, x, y):
    screen.blit(gunmanImg, (x, y))

class Gunman:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    def update(self, screen, gunmanImg):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        self.x += self.velX
        if self.x <= 0:
            self.x = 0
        elif self.x >= 768:
            self.x = 768
        self.y += self.velY
        if self.y <= 0:
            self.y = 0
        elif self.y >= 568:
            self.y = 568

        gunmanDisplay(screen, gunmanImg, self.x, self.y)
