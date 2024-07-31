import pygame
import sys
import math
import random
from gunman import Gunman
from zombie import Zombie
from safe import Zone
from upgrades import Health_Pack

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Title
pygame.display.set_caption("Boom Zombie!")

# Icon
icon = pygame.image.load('zombie.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Sound
pygame.mixer.init()
sound = pygame.mixer.Sound('hit_sound.wav')

# Gunman
gunmanImg = pygame.image.load('gunman.png')
gunmanX = int(370)
gunmanY = int(480)

# Gunman lives
lives = 5
cooldown = 2000
last_hit_time = 0

# Health Pack
health_pack = Health_Pack()
health_pack_spawned = False

# Safe Zone
safe_zone = Zone(570, 5000)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_speed = 40
bulletY_speed = 40
bulletState = "ready"

# Automatic fire rate
fire_rate = 100  # milliseconds
last_shot_time = 0

space_pressed = False

# Score
score = 0
font = pygame.font.Font(None, 36)  # Font for score display

# Round
curr_round = 1
zombies = []
num_zombies = 0
zombies_killed = 0

def bulletFire(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(zombieX, zombieY, bulletX, bulletY):
    distance = math.sqrt((math.pow(zombieX - bulletX, 2)) + (math.pow(zombieY - bulletY, 2)))
    return distance < 27

def new_round(round_num):
    global zombies, num_zombies, score, bulletState, zombies_killed, health_pack_spawned
    num_zombies = round_num * 5
    zombies_killed = 0
    zombies = [Zombie() for _ in range(num_zombies)]
    for zom in zombies:
        zom.x_speed = random.choice([2 + round_num, -(2 + round_num)])
        zom.y_speed = random.choice([2 + round_num, -(2 + round_num)])
    bulletState = "ready"  # Reset bullet state for each new round
    health_pack_spawned = False  # Reset health pack for each new round

# Gunman initialization
gunman = Gunman(gunmanX, gunmanY)

# New round (first round)
new_round(curr_round)

# Game loop
while True:
    screen.fill((0, 255, 0))  # RGB (colors)
    screen.blit(background, (0, 0))  # Background Image
    pygame.draw.line(screen, (0, 0, 0), (0, 565), (800, 565), 2)  # Safe Zone Line

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gunman.left_pressed = True
            if event.key == pygame.K_RIGHT:
                gunman.right_pressed = True
            if event.key == pygame.K_UP:
                gunman.up_pressed = True
            if event.key == pygame.K_DOWN:
                gunman.down_pressed = True
            if event.key == pygame.K_SPACE:
                space_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                gunman.left_pressed = False
            if event.key == pygame.K_RIGHT:
                gunman.right_pressed = False
            if event.key == pygame.K_UP:
                gunman.up_pressed = False
            if event.key == pygame.K_DOWN:
                gunman.down_pressed = False
            if event.key == pygame.K_SPACE:
                space_pressed = False

    # Automatic firing (logic)
    if space_pressed and bulletState == "ready" and pygame.time.get_ticks() - last_shot_time >= fire_rate:
        bulletX = gunman.x
        bulletY = gunman.y
        bulletFire(bulletX, bulletY)
        last_shot_time = pygame.time.get_ticks()

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        bulletFire(bulletX, bulletY)
        bulletY -= bulletY_speed

    # Safe Zone Validation
    prev_lives = lives
    lives, game_over = safe_zone.life_check(gunman, lives)

    if lives < prev_lives:
        sound.play()

    if game_over:
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                     screen.get_height() // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    # Display Safe Zone Stats For User
    if safe_zone.get_warning_message():
        small_font = pygame.font.Font(None, 24)  # Smaller font for warning text
        warning_lines = ["WARNING, YOU ARE NOW", f"IN THE DEAD ZONE: {safe_zone.get_time_in_safe_zone() // 1000}"]
        for i, line in enumerate(warning_lines):
            warning_text = small_font.render(line, True, (255, 0, 0))
            screen.blit(warning_text, (10, (screen.get_height() // 2) - (
                        len(warning_lines) * warning_text.get_height() // 2) + i * warning_text.get_height()))

    # Update and display zombies
    zom_remove = []
    for zombie in zombies:
        zombie.update()
        zombie.display(screen)

    # Health pack implementation (Should spawn every 1/3 rounds)
    if curr_round > 1 and curr_round % 3 == 0 and not health_pack.active and not health_pack_spawned:
        health_pack.spawn()
        health_pack_spawned = True

    # Health pack collision detection
    health_pack.display(screen)
    health_pack.update()
    if health_pack.health_collision(gunman):
        lives = 5
        sound.play()

    # Check for collisions after updating all zombies
    curr_time = pygame.time.get_ticks()
    for zombie in zombies:
        if isCollision(zombie.rect.x, zombie.rect.y, bulletX, bulletY):
            bulletY = 480
            bulletState = "ready"
            score += 1
            zombies_killed += 1
            zom_remove.append(zombie)
        elif isCollision(zombie.rect.x, zombie.rect.y, gunman.x, gunman.y) and curr_time - last_hit_time > cooldown:
            sound.play()
            lives -= 1
            last_hit_time = curr_time
            if lives <= 0:  # Game Over
                game_over_font = pygame.font.Font(None, 74)
                game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
                screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                             screen.get_height() // 2 - game_over_text.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(5000)
                pygame.quit()
                sys.exit()

    # Remove collided zombies
    for zombie in zom_remove:
        if zombie in zombies:
            zombies.remove(zombie)

    # Check for round completion
    if zombies_killed == num_zombies:
        curr_round += 1
        new_round(curr_round)

    # Display score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display round
    round_text = font.render(f'Round: {curr_round}', True, (255, 255, 255))
    screen.blit(round_text, (665, 10))

    # Display lives
    lives_text = font.render("Lives: ", True, (0, 0, 0))
    lives_text_amt = font.render(str(lives), True, (255, 0, 0))
    width = lives_text.get_width() + lives_text_amt.get_width()
    screen.blit(lives_text, (screen.get_width() // 2 - width // 2, 10))
    screen.blit(lives_text_amt, (screen.get_width() // 2 - width // 2 + lives_text.get_width(), 10))

    # Update player
    gunman.update(screen, gunmanImg)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(120)

# Test For Commit











