import pygame
import random

# Initialize pygame
pygame.init()

# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Player
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 1
GRAVITY = 0.01   
JUMP_FORCE = 4
JUMP_GRACE_PERIOD = 10
player_x = WINDOW_WIDTH / 2
player_y = WINDOW_HEIGHT / 2
player_speed_x = 0
player_speed_y = 0
on_ground = False
jump_grace_period = 0
player_power = 0
# Enemy
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_SPEED = 3
enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
enemy_y = random.randint(0, WINDOW_HEIGHT - ENEMY_HEIGHT)
# Platforms
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
platforms = [
    (200, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT), 
    (400, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT), 
    (600, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    (0, WINDOW_HEIGHT - PLATFORM_HEIGHT, WINDOW_WIDTH, PLATFORM_HEIGHT)
]
# Mushrooms
MUSHROOM_WIDTH, MUSHROOM_HEIGHT = 10, 10
mushrooms = [
    (random.randint(0, WINDOW_WIDTH - MUSHROOM_WIDTH), random.randint(0, WINDOW_HEIGHT - MUSHROOM_HEIGHT)),
    (random.randint(0, WINDOW_WIDTH - MUSHROOM_WIDTH), random.randint(0, WINDOW_HEIGHT - MUSHROOM_HEIGHT)),
    (random.randint(0, WINDOW_WIDTH - MUSHROOM_WIDTH), random.randint(0, WINDOW_HEIGHT - MUSHROOM_HEIGHT))
]
# Tokens
TOKEN_WIDTH, TOKEN_HEIGHT = 75, 75
tokens = [
    (random.randint(0, WINDOW_WIDTH - TOKEN_WIDTH), random.randint(0, WINDOW_HEIGHT - TOKEN_HEIGHT)),
    (random.randint(0, WINDOW_WIDTH - TOKEN_WIDTH), random.randint(0, WINDOW_HEIGHT - TOKEN_HEIGHT)),
    (random.randint(0, WINDOW_WIDTH - TOKEN_WIDTH), random.randint(0, WINDOW_HEIGHT - TOKEN_HEIGHT))
]
# Ui
MY_FONT = pygame.font.SysFont('Courier New', 50)
INITIAL_TOKEN_COUNT = len(tokens)

# Keep the enemy from spawning in line with the player
if enemy_y > player_y - 100 and enemy_y < player_y + 100:
    enemy_y = enemy_y + 200

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (on_ground or jump_grace_period < JUMP_GRACE_PERIOD):
                player_speed_y = -JUMP_FORCE
                jump_grace_period = JUMP_GRACE_PERIOD

    # Player movement
    player_speed_x = 0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_speed_x = -PLAYER_SPEED
    
    if keys[pygame.K_RIGHT]:
        player_speed_x = PLAYER_SPEED

    # Enemy movement
    enemy_x += ENEMY_SPEED

    if enemy_x + ENEMY_WIDTH > WINDOW_WIDTH or enemy_x < 0:
        ENEMY_SPEED = -ENEMY_SPEED

    # Apply gravity
    player_speed_y += GRAVITY
    player_x += player_speed_x
    player_y += player_speed_y

    # Collision detection
    on_ground = False
    
    # Check for collision between player and platforms
    for plat in platforms:
        if pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT).colliderect(
           pygame.Rect(plat[0], plat[1], plat[2], plat[3])):
            if player_speed_y > 0:
                player_y = plat[1] - PLAYER_HEIGHT
                player_speed_y = 0
                on_ground = True
                jump_grace_period = 0 
            
            if player_speed_y < 0:
                player_y = plat[1] + plat[3]
                player_speed_y = 0

    # Set jump grace period
    if not on_ground:
        jump_grace_period += 1

    # Check for collision between player and window
    if player_x < 0:
        player_x = 0
    
    if player_x + PLAYER_WIDTH > WINDOW_WIDTH:
        player_x = WINDOW_WIDTH - PLAYER_WIDTH

    # Check for collision between player and mushroom
    for mushroom in mushrooms[:]:
        mushroom_x, mushroom_y = mushroom

        if pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT).colliderect(
           pygame.Rect(mushroom_x, mushroom_y, MUSHROOM_WIDTH, MUSHROOM_HEIGHT)):
            mushrooms.remove(mushroom)
            player_power += 60

    # Check for collision between player and token
    for token in tokens[:]: 
        token_x, token_y = token

        if pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT).colliderect(
           pygame.Rect(token_x, token_y, TOKEN_WIDTH, TOKEN_HEIGHT)):
             tokens.remove(token)

    # Check for win condition
    if not tokens:
        print('You Win!')
        pygame.quit()

    # Check for collision between player and enemy
    if pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT).colliderect(
       pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)):
        if player_power > 0:
            player_power -= 1
            print('You lost power!')
        
        if player_power <= 0:
            print('Game Over!')
            pygame.quit()

    # Update ui values
    textsurface_score = MY_FONT.render('Score: {}'.format(str(INITIAL_TOKEN_COUNT - len(tokens)) + "/" 
    + str(INITIAL_TOKEN_COUNT)), False, (0, 255, 0))
    textsurface_lives = MY_FONT.render('Power: {}'.format(player_power), False, (0, 255, 0))

    # Draw everything
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (255, 255, 255), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
    pygame.draw.rect(window, (255, 0, 0), (enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))

    for plat in platforms:
        pygame.draw.rect(window, (0, 255, 0), (plat[0], plat[1], plat[2], plat[3]))

    for mushroom in mushrooms:
        mushroom_x, mushroom_y = mushroom
        pygame.draw.rect(window, (255, 0, 0), (mushroom_x, mushroom_y, MUSHROOM_WIDTH, MUSHROOM_HEIGHT))

    for token in tokens:
        token_x, token_y = token
        pygame.draw.rect(window, (255, 255, 0), (token_x, token_y, TOKEN_WIDTH, TOKEN_HEIGHT))

    window.blit(textsurface_score, (10, 10))
    window.blit(textsurface_lives, (10, 60))
    pygame.display.update()