import pygame
import space_invaders

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((space_invaders.width, space_invaders.height))
background = pygame.image.load('res/background.png')

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('res/icon.png')
pygame.display.set_icon(icon)

player = space_invaders.Player('res/player.png', screen)
enemy = space_invaders.Enemy('res/enemy.png', screen)
bullet = space_invaders.Bullet('res/bullet.png', screen, player)

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

    player.draw()
    enemy.draw()
    bullet.draw()

    pygame.display.update()

