import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atari Breakout")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# Font
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    """ Pomocná funkce pro vykreslení textu na obrazovku """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main_menu():
    """ Hlavní menu hry s klikacími tlačítky """
    start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50)
    quit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50)

    running = True
    while running:
        screen.fill(BLACK)

        # Vykreslení tlačítek
        pygame.draw.rect(screen, GRAY, start_button)
        pygame.draw.rect(screen, GRAY, quit_button)

        draw_text("Start Game", WIDTH//2 - 55, HEIGHT//2 - 15, BLACK)
        draw_text("Quit", WIDTH//2 - 25, HEIGHT//2 + 55, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return True  # Spustit hru
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return False  # Ukončit program

def game_loop():
    """ Hlavní herní smyčka """
    paddle_width, paddle_height = 100, 10
    paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)

    ball_radius = 8
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
    ball_speed = [random.choice([-4, 4]), -4]

    brick_rows, brick_cols = 5, 8
    brick_width = WIDTH // brick_cols
    brick_height = 20
    bricks = [pygame.Rect(col * brick_width, row * brick_height + 50, brick_width - 2, brick_height - 2)
              for row in range(brick_rows) for col in range(brick_cols)]

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Zpracování pohybu pálky
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-6, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(6, 0)

        ball.move_ip(ball_speed)

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed[1] = -ball_speed[1]
                break

        if ball.bottom >= HEIGHT:
            print("GAME OVER")
            running = False

        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, BLUE, ball)
        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)

        pygame.display.flip()
        clock.tick(60)

    pygame.time.delay(500)
    pygame.event.clear()

while main_menu():
    game_loop()
