import pygame
import os
import random

pygame.font.init()
pygame.init()

# Creating game window
WIDTH, HEIGHT = 704, 774 # 64 x 11 ~ 11x11 Tilemap
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 130, 150)
YELLOW = (240, 230, 170)
ORANGE = (220, 190, 90)

# Defining and adjusting assets
PATH = os.path.split(os.path.realpath(__file__))[0]

TILE_SIZE = 64
SNAKE_HEAD_IMAGE = pygame.image.load(os.path.join(PATH, 'Assets', 'Textures', 'Snake_Head.png'))
ORIG_SNAKE_HEAD = pygame.transform.scale(SNAKE_HEAD_IMAGE, (TILE_SIZE, TILE_SIZE))
SNAKE_HEAD = ORIG_SNAKE_HEAD.copy()

SNAKE_BODY_IMAGE = pygame.image.load(os.path.join(PATH, 'Assets', 'Textures', 'Snake_Body.png'))
ORIG_SNAKE_BODY = pygame.transform.scale(SNAKE_BODY_IMAGE, (TILE_SIZE, TILE_SIZE))
SNAKE_BODY = ORIG_SNAKE_BODY.copy()

APPLE_IMAGE = pygame.image.load(os.path.join(PATH, 'Assets', 'Textures', 'Apple.png'))
APPLE = pygame.transform.scale(APPLE_IMAGE, (TILE_SIZE, TILE_SIZE))

SCORE_FONT = pygame.font.SysFont('bahnschrift', 50)
END_SCORE_FONT = pygame.font.SysFont('bahnschrift', 100)

# IMPORTANT GAME VARIABLES
SCORE = 0
GAME_OVER = False

# Game variables



MOVE = True
MOVED = False
MOVE_TIMER = pygame.USEREVENT + 1
MOVE_INTERVAL = 200 # ms

CHANGE = False
CURR_MOVE = None

APPLE_EATEN = False

NEW_SNAKE = ()

def create_tilemap():
    TILES = []
    curr = [0, 70]
    cols = rows = int(WIDTH / TILE_SIZE)

    for r in range(rows):
        curr[0] = 0
        for c in range(cols):
            TILES.append(tuple(curr))
            curr[0] += TILE_SIZE
        curr[1] += TILE_SIZE

    TILES = tuple(TILES)

    return TILES

def move_snake(snake, p_key):
    global CHANGE
    global CURR_MOVE

    if CHANGE:
        CHANGE = False

        CURR_MOVE[0] = p_key

    global NEW_SNAKE

    new_snake_rect = snake[len(snake)-1].copy()
    new_snake_curr_move = CURR_MOVE[-1]
    NEW_SNAKE = (new_snake_rect, new_snake_curr_move)

    global MOVE
    global MOVED
    if MOVE:
        MOVE = False
        MOVED = True

        for i, value in enumerate(snake):
            rect = value
            direction = CURR_MOVE[i]

            # Move snake
            if direction == 'up':
                rect.y -= TILE_SIZE
            elif direction == 'down':
                rect.y += TILE_SIZE
            elif direction == 'right':
                rect.x += TILE_SIZE
            elif direction == 'left':
                rect.x -= TILE_SIZE
        
        pygame.time.set_timer(MOVE_TIMER, MOVE_INTERVAL)

def check_apple(snake, apple, tiles):
    snake_head = snake[0]

    global NEW_SNAKE
    global APPLE_EATEN
    global SCORE
    if snake_head.x == apple.x and snake_head.y == apple.y and APPLE_EATEN == False:
        # Eat apple and add a snake to the end of the snake
        APPLE_EATEN = True
        SCORE += 1

        snake_length = len(snake) # snake indexes + 1

        #snake[snake_length] = NEW_SNAKE[0]
        snake.append(NEW_SNAKE[0])
        CURR_MOVE.insert(-1, NEW_SNAKE[1])

        occupied_tiles = []
        for s in snake:
            tile_pos = (s.x, s.y)
            occupied_tiles.append(tile_pos)
        
        search = True
        while search:
            apple_rand_pos = tiles[random.randrange(len(tiles))]
            if apple_rand_pos not in occupied_tiles:
                search = False
        
        #apple = pygame.Rect(apple_rand_pos[0], apple_rand_pos[1], TILE_SIZE, TILE_SIZE)
        apple.x, apple.y = apple_rand_pos[0], apple_rand_pos[1]

def check_death(snake, tiles):
    global GAME_OVER
    if GAME_OVER == False:
        snake_head = snake[0].copy()
        snake_body = snake.copy(); del snake_body[0]
        
        hit_self = False
        out_of_bounds = False
        
        # Check if snake hit it's own tail/body
        for s in snake_body:
            if snake_head.x == s.x and snake_head.y == s.y:
                hit_self = True
                break
        
        # Check if snake is out of bounds
        if snake_head.y < 70:
            out_of_bounds = True
        elif snake_head.y > HEIGHT - TILE_SIZE:
            out_of_bounds = True
        elif snake_head.x < 0:
            out_of_bounds = True
        elif snake_head.x > WIDTH - TILE_SIZE:
            out_of_bounds = True
        
        if hit_self or out_of_bounds:
            GAME_OVER = True

def draw_window(snake, apple, tiles):
    # Background
    WIN.fill(WHITE)
    # Scoreboard background
    pygame.draw.rect(WIN, BLUE, (0, 0, WIDTH, 70))
    # Scoreboard and background split
    pygame.draw.rect(WIN, BLACK, (0, 67, WIDTH, 3))

    # Scoreboard Text
    score_text = SCORE_FONT.render(f'Score: {str(SCORE)}', 1, WHITE)
    WIN.blit(score_text, (10, 35 - score_text.get_height() // 2 + 2))

    # Tilemap
    for i, tile in enumerate(tiles):
        if i % 2 == 0:
            color = ORANGE
        else:
            color = YELLOW
        
        pygame.draw.rect(WIN, color, (tile[0], tile[1], TILE_SIZE, TILE_SIZE))

    if GAME_OVER == False:
        # Snake
        snake_rev = snake[::-1]
        curr_move_rev = CURR_MOVE[::-1]

        for i, value in enumerate(snake_rev):
            rect = value
            if i == len(snake_rev) - 1:
                img = SNAKE_HEAD.copy()
            else:
                img = SNAKE_BODY.copy()
            
            m_next = curr_move_rev[i]

            if m_next == 'up':
                img = pygame.transform.rotate(img, 0)
            elif m_next == 'down':
                img = pygame.transform.rotate(img, 180)
            elif m_next == 'right':
                img = pygame.transform.rotate(img, 270)
            elif m_next == 'left':
                img = pygame.transform.rotate(img, 90)
            
            WIN.blit(img, (rect.x, rect.y))
        
        global MOVED
        if MOVED:
            MOVED = False
            del CURR_MOVE[-1]
            CURR_MOVE.insert(0, CURR_MOVE[0])
        
        # Apple
        WIN.blit(APPLE, (apple.x, apple.y))
    else:
        black_bg = pygame.Surface((WIDTH, HEIGHT))
        black_bg.set_alpha(180)
        WIN.blit(black_bg, (0, 0))
        # End Score Text
        end_score_text = END_SCORE_FONT.render(f'Score: {str(SCORE)}', 1, WHITE)
        WIN.blit(end_score_text, ((WIDTH - end_score_text.get_width()) // 2, (HEIGHT - end_score_text.get_height()) // 2 + 35))

    pygame.display.update()

def main():
    snake_tiles = [
        pygame.Rect(512, 390, TILE_SIZE, TILE_SIZE),
        pygame.Rect(512, 454, TILE_SIZE, TILE_SIZE),
        pygame.Rect(512, 518, TILE_SIZE, TILE_SIZE)
    ]

    global CURR_MOVE
    CURR_MOVE = ['left', 'up', 'up']
    has_changed = False
    key_pressed = None

    apple = pygame.Rect(320, 134, TILE_SIZE, TILE_SIZE)

    tiles = create_tilemap()

    clock = pygame.time.Clock()
    run = True
    while run:
        # Setting FPS cap
        clock.tick(60)

        # Check if game should be closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == MOVE_TIMER:
                global MOVE
                global APPLE_EATEN
                MOVE = True
                APPLE_EATEN = False
                has_changed = False
            elif event.type == pygame.KEYDOWN and has_changed == False:
                p_keys = {pygame.K_w: 'up', pygame.K_s: 'down', pygame.K_a: 'left', pygame.K_d: 'right'}
                if event.key in p_keys.keys():
                    key_pressed = p_keys[event.key]
                    opp_keys = {'down': 'up', 'up': 'down', 'left': 'right', 'right': 'left'}
                    if key_pressed != opp_keys[CURR_MOVE[0]] and key_pressed != CURR_MOVE[0]:
                        global CHANGE
                        CHANGE = True
                        has_changed = True
        if GAME_OVER == False:
            # Move the snake
            move_snake(snake_tiles, key_pressed)

            # Eat the apple
            check_apple(snake_tiles, apple, tiles)

            # Check for death
            check_death(snake_tiles, tiles)

            # Update window
            draw_window(snake_tiles, apple, tiles)

    pygame.quit()

if __name__ == '__main__':
    main()