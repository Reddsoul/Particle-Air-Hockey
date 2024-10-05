# helpers.py

import pygame
from constants import WHITE, BLACK, MALLET_RADIUS, BALL_RADIUS, BALL_SPEED_X, BALL_SPEED_Y

def draw_mallets(screen, mallet1_x, mallet1_y, mallet2_x, mallet2_y):
    pygame.draw.circle(screen, WHITE, (int(mallet1_x), int(mallet1_y)), MALLET_RADIUS)
    pygame.draw.circle(screen, WHITE, (int(mallet2_x), int(mallet2_y)), MALLET_RADIUS)

def draw_ball(screen, ball_x, ball_y):
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

def draw_middle_line(screen, WIDTH, HEIGHT):
    for i in range(10, HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, i), (WIDTH // 2, i + 20), 2)

def reset_ball_and_mallets(WIDTH, HEIGHT, particles, scoring_player=None):
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_vy = BALL_SPEED_Y
    mallet1_x, mallet1_y = WIDTH // 4, HEIGHT // 2
    mallet2_x, mallet2_y = 3 * WIDTH // 4, HEIGHT // 2
    game_over = False
    winner = None
    particles.clear()  # Clear all particles on reset
    if scoring_player == 1:
        ball_vx = BALL_SPEED_X  # Move towards Player 2
    elif scoring_player == 2:
        ball_vx = -BALL_SPEED_X  # Move towards Player 1
    else:
        ball_vx = BALL_SPEED_X  # Reset to default direction
    return ball_x, ball_y, ball_vx, ball_vy, mallet1_x, mallet1_y, mallet2_x, mallet2_y, game_over, winner

def show_start_screen(screen, WIDTH, HEIGHT):
    show_screen = True
    while show_screen:
        screen.fill(BLACK)
        # Display the controls
        font = pygame.font.Font(None, 36)
        controls = [
            "Air Hockey Game Controls",
            "",
            "Player 1 (Left Mallet):",
            "  W - Move Up",
            "  S - Move Down",
            "  A - Move Left",
            "  D - Move Right",
            "",
            "Player 2 (Right Mallet):",
            "  I - Move Up",
            "  K - Move Down",
            "  J - Move Left",
            "  L - Move Right",
            "",
            "Other Controls:",
            "  SPACE - Start/Resume Game",
            "  R - Reset Game",
            "  ESC - Quit Game",
            "",
            "Trail Modes:",
            "  1 - Simple Trail Mode",
            "  2 - Complex Trail Mode",
            "  0 - Disable Trail",
            "",
            "Press SPACE to start the game.",
        ]
        y_offset = 50
        for line in controls:
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30  # Adjust as needed

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_screen = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    return WIDTH, HEIGHT