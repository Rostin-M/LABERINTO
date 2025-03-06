import pygame
import time
from settings import WIDTH, HEIGHT, WHITE, BLACK, MONSTER_SPEED, NUM_MONSTERS
from maze import generate_maze, Player, Monster

def handle_game_events(player, maze):
    # Maneja los eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: player.move(-1, 0, maze)
            if event.key == pygame.K_RIGHT: player.move(1, 0, maze)
            if event.key == pygame.K_UP: player.move(0, -1, maze)
            if event.key == pygame.K_DOWN: player.move(0, 1, maze)
    return True

def draw_game(screen, maze, player, goal, monsters):
    # Dibuja el estado actual del juego
    screen.fill(WHITE)
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * 30, row * 30, 30, 30))
    pygame.draw.rect(screen, (0, 255, 0), goal)
    player.draw(screen)

    for monster in monsters:
        monster.draw(screen)

    pygame.display.flip()

def run_game():
    # Ejecuta el bucle principal del juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape del Laberinto")

    maze = generate_maze()
    player = Player()
    goal = pygame.Rect(570, 570, 30, 30)
    monsters = [Monster(maze) for _ in range(NUM_MONSTERS)]

    running = True
    while running:
        running = handle_game_events(player, maze)

        for monster in monsters:
            monster.move(maze)

        for monster in monsters:
            if player.rect.colliderect(monster.rect):
                show_loss_screen(screen)
                return

        if player.rect.colliderect(goal):
            show_win_screen(screen, round(time.time() - player.start_time, 2), player.moves)
            return

        draw_game(screen, maze, player, goal, monsters)
        pygame.time.delay(200)

def show_win_screen(screen, time_taken, moves):
    # Muestra la pantalla de victoria
    pygame.mixer.music.load("win_sound.wav")
    pygame.mixer.music.play()

    font_big = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    for i in range(HEIGHT):
        color = (0, 150 + i // 6, 255)
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

    text1 = font_big.render("¡Ganaste!", True, WHITE)
    text2 = font_small.render("Presiona una tecla para continuar", True, WHITE)

    x_center = WIDTH // 2
    y_center = HEIGHT // 3

    screen.blit(text1, (x_center - text1.get_width() // 2, y_center))
    screen.blit(text2, (x_center - text2.get_width() // 2, y_center + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                waiting = False

    from menu import menu
    menu()

def show_loss_screen(screen):
    # Muestra la pantalla de derrota
    pygame.mixer.music.load("lose_sound.wav")
    pygame.mixer.music.play()

    font = pygame.font.Font(None, 50)
    screen.fill((200, 0, 0))

    text1 = font.render("¡Has sido atrapado ! :( ", True, WHITE)
    text2 = font.render("Presiona cualquier tecla para volver", True, WHITE)

    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                waiting = False

    from menu import menu
    menu()