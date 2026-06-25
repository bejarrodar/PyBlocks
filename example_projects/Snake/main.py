# Snake Game — use arrow keys to move, eat the red food!  # __pyblocks_id__:sn0
import pygame  # __pyblocks_id__:sn1
import random  # __pyblocks_id__:sn2
# Constants  # __pyblocks_id__:sn3
CELL = 20  # __pyblocks_id__:sn4
COLS = 30  # __pyblocks_id__:sn5
ROWS = 20  # __pyblocks_id__:sn6
WIDTH = CELL * COLS  # __pyblocks_id__:sn7
HEIGHT = CELL * ROWS  # __pyblocks_id__:sn8
FPS = 8  # __pyblocks_id__:sn9
# Colors (R, G, B)  # __pyblocks_id__:sn10
BLACK = (0, 0, 0)  # __pyblocks_id__:sn11
GREEN = (0, 180, 0)  # __pyblocks_id__:sn12
RED = (200, 0, 0)  # __pyblocks_id__:sn13
# Set up the pygame window  # __pyblocks_id__:sn14
pygame.init()  # __pyblocks_id__:sn15
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # __pyblocks_id__:sn16
pygame.display.set_caption("Snake")  # __pyblocks_id__:sn17
clock = pygame.time.Clock()  # __pyblocks_id__:sn18
# Game state  # __pyblocks_id__:sn19
snake = [(COLS // 2, ROWS // 2)]  # __pyblocks_id__:sn20
dx = 1  # __pyblocks_id__:sn21
dy = 0  # __pyblocks_id__:sn22
food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))  # __pyblocks_id__:sn23
running = True  # __pyblocks_id__:sn24
score = 0  # __pyblocks_id__:sn25
# Game loop  # __pyblocks_id__:sn26
while running:  # __pyblocks_id__:sn27
    for event in pygame.event.get():  # __pyblocks_id__:sn27c0
        if event.type == pygame.QUIT:  # __pyblocks_id__:sn27c0c0
            running = False  # __pyblocks_id__:sn27c0c0c0
        if event.type == pygame.KEYDOWN:  # __pyblocks_id__:sn27c0c1
            if event.key == pygame.K_UP and dy == 0:  # __pyblocks_id__:sn27c0c1c0
                dx, dy = 0, -1  # __pyblocks_id__:sn27c0c1c0c0
            elif event.key == pygame.K_DOWN and dy == 0:  # __pyblocks_id__:sn27c0c1c1
                dx, dy = 0, 1  # __pyblocks_id__:sn27c0c1c1c0
            elif event.key == pygame.K_LEFT and dx == 0:  # __pyblocks_id__:sn27c0c1c2
                dx, dy = -1, 0  # __pyblocks_id__:sn27c0c1c2c0
            elif event.key == pygame.K_RIGHT and dx == 0:  # __pyblocks_id__:sn27c0c1c3
                dx, dy = 1, 0  # __pyblocks_id__:sn27c0c1c3c0
    # Move the snake head one step  # __pyblocks_id__:sn27c1
    hx = snake[0][0] + dx  # __pyblocks_id__:sn27c2
    hy = snake[0][1] + dy  # __pyblocks_id__:sn27c3
    if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:  # __pyblocks_id__:sn27c4
        running = False  # __pyblocks_id__:sn27c4c0
    if (hx, hy) in snake:  # __pyblocks_id__:sn27c5
        running = False  # __pyblocks_id__:sn27c5c0
    if (hx, hy) == food:  # __pyblocks_id__:sn27c6
        score += 1  # __pyblocks_id__:sn27c6c0
        food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))  # __pyblocks_id__:sn27c6c1
    else:  # __pyblocks_id__:sn27c7
        snake.pop()  # __pyblocks_id__:sn27c7c0
    snake.insert(0, (hx, hy))  # __pyblocks_id__:sn27c8
    # Draw everything  # __pyblocks_id__:sn27c9
    screen.fill(BLACK)  # __pyblocks_id__:sn27c10
    for seg in snake:  # __pyblocks_id__:sn27c11
        pygame.draw.rect(screen, GREEN, (seg[0] * CELL, seg[1] * CELL, CELL - 2, CELL - 2))  # __pyblocks_id__:sn27c11c0
    pygame.draw.rect(screen, RED, (food[0] * CELL, food[1] * CELL, CELL - 2, CELL - 2))  # __pyblocks_id__:sn27c12
    pygame.display.set_caption(f"Snake  Score: {score}")  # __pyblocks_id__:sn27c13
    pygame.display.flip()  # __pyblocks_id__:sn27c14
    clock.tick(FPS)  # __pyblocks_id__:sn27c15
pygame.quit()  # __pyblocks_id__:sn28