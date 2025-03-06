import pygame
import random
import time
from settings import WIDTH, HEIGHT, TILE_SIZE, ROWS, COLS, WHITE, BLACK, BLUE, GREEN, RED, DIRECTIONS, MONSTER_SPEED

def generate_maze():
    # Genera un laberinto con paredes (1) y caminos (0)
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    walls = []
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    for dx, dy in DIRECTIONS:
        nx, ny = start_x + dx, start_y + dy
        if 1 <= nx < COLS - 1 and 1 <= ny < ROWS - 1:
            walls.append((nx, ny, start_x, start_y))
    
    while walls:
        wx, wy, px, py = random.choice(walls)
        walls.remove((wx, wy, px, py))

        if maze[wy][wx] == 1:
            maze[wy][wx] = 0
            maze[(wy + py) // 2][(wx + px) // 2] = 0

            for dx, dy in DIRECTIONS:
                nx, ny = wx + dx, wy + dy
                if 1 <= nx < COLS - 1 and 1 <= ny < ROWS - 1:
                    walls.append((nx, ny, wx, wy))

    # Ajuste para que la salida esté en la esquina superior izquierda y este libre a sus alrededores
    exit_x, exit_y = COLS - 2, ROWS - 2
    maze[exit_y][exit_x] = 0
    maze[exit_y - 1][exit_x] = 0
    maze[exit_y + 1][exit_x] = 0
    maze[exit_y][exit_x - 1] = 0
    maze[exit_y][exit_x + 1] = 0
    maze[exit_y - 1][exit_x - 1] = 0
    maze[exit_y - 1][exit_x + 1] = 0
    maze[exit_y + 1][exit_x - 1] = 0
    maze[exit_y + 1][exit_x + 1] = 0

    return maze

class Player:
    def __init__(self):
        # Inicializa el jugador
        self.x, self.y = 1, 1
        self.color = BLUE
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.moves = 0
        self.start_time = time.time()
    
    def move(self, dx, dy, maze):
        # Mueve al jugador si la nueva posición es válida
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
            self.moves += 1
    
    def draw(self, screen):
        # Dibuja al jugador en la pantalla
        pygame.draw.rect(screen, self.color, self.rect)

class Monster:
    def __init__(self, maze):
        # Inicializa el monstruo en una posición válida
        while True:
            self.x = random.randint(1, COLS - 2)
            self.y = random.randint(1, ROWS - 2)
            if maze[self.y][self.x] == 0:
                break
        self.color = RED
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.direction = random.choice(DIRECTIONS)
        self.last_move_time = pygame.time.get_ticks()

    def move(self, maze):
        # Mueve al monstruo si ha pasado suficiente tiempo
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= MONSTER_SPEED:
            new_x, new_y = self.x + self.direction[0] // 2, self.y + self.direction[1] // 2
            if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
                self.x, self.y = new_x, new_y
            else:
                self.direction = random.choice(DIRECTIONS)
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
            self.last_move_time = current_time

    def draw(self, screen):
        # Dibuja al monstruo en la pantalla
        pygame.draw.rect(screen, self.color, self.rect)