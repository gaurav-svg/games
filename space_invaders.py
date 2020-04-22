import sys
import pygame
from pygame import mixer
import random
import math

bullet_state = "ready"


def play_game():
    # Initialize the game
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Alien Invasion')

    # adding the game icon on top
    icon = pygame.image.load('spaceship.png')
    pygame.display.set_icon(icon)

    # creating the background image
    background = pygame.image.load('background.jpg')

    # Background sound
    mixer.music.load('backgroundsound.wav')
    mixer.music.play(-1)  # here the -1 is used continuously play the sound or else it
    # it would have played only once and stopped

    # adding the player image at the desired location
    player_img = pygame.image.load('space-invaders (1).png')
    player_x = 370
    player_y = 480
    player_x_change = 0

    # adding the enemy image
    enemy_img = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load('alien.png'))
        enemy_x.append(random.randint(0, 735))  # the two arguments given are the starting value and the ending value
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(2)
        enemy_y_change.append(40)

    # adding the image of bullet
    # Ready - you can't see the bullet on the screen
    # Fire -The bullet is currently moving
    bullet_img = pygame.image.load('bullet.png')
    bullet_x = 0
    bullet_y = 480
    bullet_x_change = 0
    bullet_y_change = 15

    # score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textx = 10
    texty = 10

    # Game over text
    over_font = pygame.font.Font('freesansbold.ttf', 80)

    def show_score(x, y):
        score = font.render("score :" + str(score_value), True, (255, 200, 200))

        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 10, 0))
        screen.blit(over_text, (200, 250))

    def player(x, y):
        screen.blit(player_img, (x, y))

    def enemy(x, y, i):
        screen.blit(enemy_img[i], (x, y))

    bg_color = (210, 150, 75)

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bullet_img, (x + 16, y + 10))

    def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
        distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
        if distance < 27:
            return True

    while True:
        global bullet_state

        screen.fill(bg_color)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_x_change = 5

                if event.key == pygame.K_LEFT:
                    player_x_change = -5

                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        # to get the current x-coordinate of the bullet
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player_x_change = 0

        player_x += player_x_change

        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # enemy movement
        for i in range(num_of_enemies):

            # Game over
            if enemy_y[i] > 440:
                for j in range(num_of_enemies):
                    enemy_y[j] = 2000
                game_over_text()
                break

            enemy_x[i] += enemy_x_change[i]

            if enemy_x[i] <= 0:
                enemy_x_change[i] = 2
                enemy_y[i] += enemy_y_change[i]

            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -2
                enemy_y[i] += enemy_y_change[i]

            # Collision
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1

                enemy_x[i] = random.randint(0, 735)
                enemy_y[i] = random.randint(50, 150)

            enemy(enemy_x[i], enemy_y[i], i)

        # bullet movement

        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score(textx, texty)
        pygame.display.update()


play_game()
