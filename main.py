# main.py

import pygame
import random
from constants import *
from particle import *
from utils import *

# Initialize Pygame
pygame.init()

# Create the screen with the RESIZABLE flag
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Air Hockey Particles")

# Current screen dimensions
WIDTH, HEIGHT = DEFAULT_WIDTH, DEFAULT_HEIGHT

# Initialize game objects and variables
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_vx = BALL_SPEED_X
ball_vy = BALL_SPEED_Y
mallet1_x, mallet1_y = WIDTH // 4, HEIGHT // 2
mallet2_x, mallet2_y = 3 * WIDTH // 4, HEIGHT // 2
score1 = 0
score2 = 0
game_over = False
winner = None
trail_mode = 0  # 0 = No trail, 1 = Simple, 2 = Complex
particles = []

# Show the start screen before the game loop
WIDTH, HEIGHT = show_start_screen(screen, WIDTH, HEIGHT)

# Game loop
running = True
while running:
    pygame.time.delay(30)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                (
                    ball_x,
                    ball_y,
                    ball_vx,
                    ball_vy,
                    mallet1_x,
                    mallet1_y,
                    mallet2_x,
                    mallet2_y,
                    game_over,
                    winner,
                ) = reset_ball_and_mallets(WIDTH, HEIGHT, particles)
                GAME_STARTED = False
            if event.key == pygame.K_SPACE:
                if game_over:
                    (
                        ball_x,
                        ball_y,
                        ball_vx,
                        ball_vy,
                        mallet1_x,
                        mallet1_y,
                        mallet2_x,
                        mallet2_y,
                        game_over,
                        winner,
                    ) = reset_ball_and_mallets(WIDTH, HEIGHT, particles)
                    GAME_STARTED = False
                else:
                    GAME_STARTED = True
            if event.key == pygame.K_1:
                trail_mode = 1  # Simple mode
            if event.key == pygame.K_2:
                trail_mode = 2  # Complex mode
            if event.key == pygame.K_0:
                trail_mode = 0  # No trail, clear particles
                particles.clear()
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            # Adjust positions relative to new window size
            ball_x = WIDTH / DEFAULT_WIDTH * ball_x
            ball_y = HEIGHT / DEFAULT_HEIGHT * ball_y
            mallet1_x = WIDTH / DEFAULT_WIDTH * mallet1_x
            mallet1_y = HEIGHT / DEFAULT_HEIGHT * mallet1_y
            mallet2_x = WIDTH / DEFAULT_WIDTH * mallet2_x
            mallet2_y = HEIGHT / DEFAULT_HEIGHT * mallet2_y
            DEFAULT_WIDTH, DEFAULT_HEIGHT = WIDTH, HEIGHT

    # Add particles based on mode
    if trail_mode > 0 and GAME_STARTED:
        if trail_mode == 1:  # Simple mode
            size = BALL_RADIUS
            x = ball_x
            y = ball_y
            color = (255, 255, 255)  # White
        else:  # Complex mode
            size = random.randint(BALL_RADIUS // 2, BALL_RADIUS * 2)
            # Random offset from ball position
            x = ball_x + random.randint(-10, 10)
            y = ball_y + random.randint(-10, 10)
            # Random color between yellow and orange
            color = (255, random.randint(100, 200), 0)  # Shades between yellow and orange
        transparency = 255
        lifespan = 25
        new_particle = Particle(x, y, size, lifespan, transparency, color, trail_mode)
        particles.append(new_particle)

    # Handle mallet movement for Player 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and mallet1_y > MALLET_RADIUS:  # Move up
        mallet1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and mallet1_y < HEIGHT - MALLET_RADIUS:  # Move down
        mallet1_y += PADDLE_SPEED
    if keys[pygame.K_a] and mallet1_x > MALLET_RADIUS:  # Move left
        mallet1_x -= PADDLE_SPEED
    if (
        keys[pygame.K_d] and mallet1_x < WIDTH // 2 - MALLET_RADIUS
    ):  # Move right, but not past the middle
        mallet1_x += PADDLE_SPEED

    # Handle mallet movement for Player 2
    if keys[pygame.K_i] and mallet2_y > MALLET_RADIUS:  # Move up
        mallet2_y -= PADDLE_SPEED
    if keys[pygame.K_k] and mallet2_y < HEIGHT - MALLET_RADIUS:  # Move down
        mallet2_y += PADDLE_SPEED
    if (
        keys[pygame.K_j] and mallet2_x > WIDTH // 2 + MALLET_RADIUS
    ):  # Move left, but not past the middle
        mallet2_x -= PADDLE_SPEED
    if keys[pygame.K_l] and mallet2_x < WIDTH - MALLET_RADIUS:  # Move right
        mallet2_x += PADDLE_SPEED

    # Update ball position
    if GAME_STARTED:
        ball_x += ball_vx
        ball_y += ball_vy

    # Ball collision with top and bottom walls
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_vy = -ball_vy  # Reverse the vertical direction

    # Ball collision with mallet1
    dx = ball_x - mallet1_x
    dy = ball_y - mallet1_y
    distance_sq = dx * dx + dy * dy
    combined_radius = BALL_RADIUS + MALLET_RADIUS
    if distance_sq <= combined_radius * combined_radius and distance_sq != 0:
        distance = distance_sq ** 0.5
        nx = dx / distance
        ny = dy / distance
        dot = ball_vx * nx + ball_vy * ny
        ball_vx = ball_vx - 2 * dot * nx
        ball_vy = ball_vy - 2 * dot * ny
        # Adjust position to prevent overlap
        overlap = combined_radius - distance
        ball_x += nx * overlap
        ball_y += ny * overlap

    # Ball collision with mallet2
    dx = ball_x - mallet2_x
    dy = ball_y - mallet2_y
    distance_sq = dx * dx + dy * dy
    if distance_sq <= combined_radius * combined_radius and distance_sq != 0:
        distance = distance_sq ** 0.5
        nx = dx / distance
        ny = dy / distance
        dot = ball_vx * nx + ball_vy * ny
        ball_vx = ball_vx - 2 * dot * nx
        ball_vy = ball_vy - 2 * dot * ny
        # Adjust position to prevent overlap
        overlap = combined_radius - distance
        ball_x += nx * overlap
        ball_y += ny * overlap

    # Clamp ball velocity to prevent it from going too fast
    speed_sq = ball_vx * ball_vx + ball_vy * ball_vy
    if speed_sq > MAX_BALL_SPEED * MAX_BALL_SPEED:
        scale = MAX_BALL_SPEED / (speed_sq ** 0.5)
        ball_vx *= scale
        ball_vy *= scale

    # Check for goals
    if ball_x - BALL_RADIUS <= 0:
        score2 += 1
        (
            ball_x,
            ball_y,
            ball_vx,
            ball_vy,
            mallet1_x,
            mallet1_y,
            mallet2_x,
            mallet2_y,
            game_over,
            winner,
        ) = reset_ball_and_mallets(WIDTH, HEIGHT, particles, scoring_player=2)
        GAME_STARTED = False  # Stop the game after a goal
    if ball_x + BALL_RADIUS >= WIDTH:
        score1 += 1
        (
            ball_x,
            ball_y,
            ball_vx,
            ball_vy,
            mallet1_x,
            mallet1_y,
            mallet2_x,
            mallet2_y,
            game_over,
            winner,
        ) = reset_ball_and_mallets(WIDTH, HEIGHT, particles, scoring_player=1)
        GAME_STARTED = False  # Stop the game after a goal

    # Check for a winner
    if score1 >= WINNING_SCORE:
        game_over = True
        winner = "Player 1"
    elif score2 >= WINNING_SCORE:
        game_over = True
        winner = "Player 2"

    # Update and render particles
    for particle in particles[:]:
        particle.update()
        if particle.is_dead():
            particles.remove(particle)

    # Draw everything
    screen.fill(BLACK)
    draw_middle_line(screen, WIDTH, HEIGHT)
    draw_mallets(screen, mallet1_x, mallet1_y, mallet2_x, mallet2_y)
    draw_ball(screen, ball_x, ball_y)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Display the scores
    font = pygame.font.Font(None, 74)
    # Player 1 Score
    text1 = font.render(str(score1), True, WHITE)
    x1 = WIDTH * 0.25 - text1.get_width() // 2
    screen.blit(text1, (x1, 10))
    # Player 2 Score
    text2 = font.render(str(score2), True, WHITE)
    x2 = WIDTH * 0.75 - text2.get_width() // 2
    screen.blit(text2, (x2, 10))

    # Display the winner if the game is over
    if game_over:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        win_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(
            win_text,
            (
                WIDTH // 2 - win_text.get_width() // 2,
                HEIGHT // 2 - win_text.get_height() // 2,
            ),
        )

    # Update display
    pygame.display.flip()

pygame.quit()