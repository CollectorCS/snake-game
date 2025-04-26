import pygame
import random
import sys

print("Initializing Pygame...")

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize score variables
score = 0
high_score = 0

# Load high score from file
def load_high_score():
    global high_score
    try:
        print("Loading high score from file...")
        with open("high_score.txt", "r") as f:
            high_score = int(f.read())
        print(f"Loaded high score: {high_score}")
    except FileNotFoundError:
        high_score = 0
        print("High score file not found. Setting high score to 0.")

# Save high score to file
def save_high_score():
    try:
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))
        print(f"High score saved: {high_score}")
    except Exception as e:
        print(f"Error saving high score: {e}")

# The rest of the code follows...



import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize score variables
score = 0
high_score = 0

# Load high score from file
def load_high_score():
    global high_score
    try:
        with open("high_score.txt", "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0

# Save high score to file
def save_high_score():
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

# Snake setup
snake = [(100, 100)]
snake_dir = (CELL_SIZE, 0)  # Moving right initially

# Food setup
def random_food():
    return (
        random.randint(1, (WIDTH - CELL_SIZE) // CELL_SIZE - 1) * CELL_SIZE,
        random.randint(1, (HEIGHT - CELL_SIZE) // CELL_SIZE - 1) * CELL_SIZE,
    )

food = random_food()

# Show start screen
def start_screen():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press SPACE to Start", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    waiting = True
    while waiting:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Game over screen
def game_over_screen():
    global score, high_score

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    restart_button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 50, 160, 40)

    # Update high score
    if score > high_score:
        high_score = score
        save_high_score()

    for seconds_left in range(10, 0, -1):
        screen.fill(BLACK)

        game_over_text = font.render("Game Over!", True, RED)
        countdown_text = small_font.render(f"Closing in {seconds_left}...", True, WHITE)

        # Draw the button
        pygame.draw.rect(screen, (0, 255, 0), restart_button_rect)
        restart_text = small_font.render("Restart", True, BLACK)
        screen.blit(restart_text, restart_text.get_rect(center=restart_button_rect.center))

        # Draw score and high score
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        high_score_text = small_font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Calculate the width of the high score text and adjust position
        high_score_width = high_score_text.get_width()
        screen.blit(high_score_text, (WIDTH - high_score_width - 10, 10))

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(countdown_text, countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Restart game on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    game_loop()

        pygame.time.delay(1000)  # 1 second delay

    pygame.quit()
    sys.exit()

# Main game loop
def game_loop():
    global snake, snake_dir, food, score

    snake[:] = [(100, 100)]
    snake_dir = (CELL_SIZE, 0)
    food = random_food()
    score = 0  # Reset score
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                    snake_dir = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                    snake_dir = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                    snake_dir = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                    snake_dir = (CELL_SIZE, 0)

                # WASD controls
                elif event.key == pygame.K_w and snake_dir != (0, CELL_SIZE):
                    snake_dir = (0, -CELL_SIZE)
                elif event.key == pygame.K_s and snake_dir != (0, -CELL_SIZE):
                    snake_dir = (0, CELL_SIZE)
                elif event.key == pygame.K_a and snake_dir != (CELL_SIZE, 0):
                    snake_dir = (-CELL_SIZE, 0)
                elif event.key == pygame.K_d and snake_dir != (-CELL_SIZE, 0):
                    snake_dir = (CELL_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, new_head)

        # Check collision with food
        if new_head == food:
            food = random_food()
            score += 10  # Increase score when food is eaten
        else:
            snake.pop()

        # Check collisions (wall or self)
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH
            or new_head[1] < 0 or new_head[1] >= HEIGHT
            or new_head in snake[1:]
        ):
            game_over_screen()

        # Draw everything
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # Draw score
        font = pygame.font.SysFont(None, 32)
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Calculate the width of the high score text and adjust position
        high_score_width = high_score_text.get_width()
        screen.blit(high_score_text, (WIDTH - high_score_width - 10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    load_high_score()
    start_screen()
    game_loop()
