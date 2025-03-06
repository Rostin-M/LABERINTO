import pygame
import sys
from settings import WIDTH, HEIGHT, WHITE, GRAY, BLACK
from ui import Button
from game import run_game

def exit_game():
    pygame.quit()
    sys.exit()

def get_latest_stats():
    """Lee las estadísticas más recientes desde stats.txt"""
    try:
        with open("stats.txt", "r") as file:
            stats = file.read().splitlines()
        last_time = stats[0] if stats else "N/A"
        last_moves = stats[1] if len(stats) > 1 else "N/A"
    except FileNotFoundError:
        last_time, last_moves = "N/A", "N/A"
    
    return last_time, last_moves

def menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menú - Laberinto")

    logo = pygame.image.load("images/logo_laberinto.png")
    logo = pygame.transform.scale(logo, (250, 120))

    font = pygame.font.Font(None, 40)
    logo_y = 30
    stats_y = logo_y + logo.get_height() + 20
    buttons_y = stats_y + 100

    button_width, button_height = 150, 50
    play_button = Button(WIDTH // 2 - button_width // 2, buttons_y, button_width, button_height, "Jugar", GRAY, run_game)
    exit_button = Button(WIDTH // 2 - button_width // 2, buttons_y + 70, button_width, button_height, "Salir", (200, 0, 0), exit_game)

    running = True
    while running:
        screen.fill(WHITE)
        last_time, last_moves = get_latest_stats()

        screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, logo_y))

        time_text = font.render(f"Último tiempo: {last_time} seg", True, BLACK)
        moves_text = font.render(f"Últimos movimientos: {last_moves}", True, BLACK)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, stats_y))
        screen.blit(moves_text, (WIDTH // 2 - moves_text.get_width() // 2, stats_y + 40))

        play_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            play_button.check_click(event)
            exit_button.check_click(event)
