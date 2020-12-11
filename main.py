import pygame
from pygame import mixer
import space_invaders

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((space_invaders.width, space_invaders.height))
background = pygame.image.load('res/background.png')

# Sound
mixer.music.load('res/background.wav')
mixer.music.play(-1) # Loop

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('res/icon.png')
pygame.display.set_icon(icon)

# Create items
player = space_invaders.Player('res/player.png', screen)
num_of_enemies = 5
enemies = []
for i in range(num_of_enemies):
    enemies.append(space_invaders.Enemy('res/enemy.png', screen))
bullet = space_invaders.Bullet('res/bullet.png', screen, player)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render(f'Score: {score_value}', True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game loop
running = True
while running:
    screen.fill((26, 5, 28))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(space_invaders.Direction.LEFT)
            if event.key == pygame.K_RIGHT:
                player.move(space_invaders.Direction.RIGHT)
            if event.key == pygame.K_SPACE:
                bullet.fire()
        if event.type == pygame.KEYUP:
            player.stop()

    for enemy in enemies:
        if space_invaders.is_collision(enemy, bullet):
            bullet.hit()
            enemy.hit()
            score_value += 1
        if space_invaders.is_over(enemy, player):
            space_invaders.game_over(screen)
            break

    player.draw()
    for enemy in enemies:
        enemy.draw()
    bullet.draw()
    show_score(text_x, text_y)

    pygame.display.update()
