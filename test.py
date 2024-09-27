import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размер окна
window_size = 600
tile_size = 40  # Размер одной клетки карты
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()

# Задание цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

# Карта уровня (двумерный массив)
level_map = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", "#", ".", "C", ".", ".", ".", ".", "C", ".", "#"],
    ["#", ".", "#", ".", "#", ".", "#", "#", "#", "#", ".", "#", ".", "#"],
    ["#", ".", "#", ".", ".", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", "#", "#", "#", "#", "#", ".", "#", "#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#", ".", "#", ".", "#"],
    ["#", "C", "#", "#", "#", ".", "#", "#", ".", "#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", "#", ".", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "E", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

# Начальная позиция игрока
player_x = 1
player_y = 1
player_speed = 4  # Скорость движения игрока
moving = False  # Флаг для проверки движения

# Функция для рисования карты
def draw_map():
    for y in range(len(level_map)):
        for x in range(len(level_map[0])):
            tile = level_map[y][x]
            if tile == "#":  # Стена
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            elif tile == ".":  # Свободное пространство
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            elif tile == "C":  # Монетка
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
                pygame.draw.circle(screen, GOLD, (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2), tile_size // 4)
            elif tile == "P":  # Игрок
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
                pygame.draw.circle(screen, BLACK, (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2), tile_size // 3)
            elif tile == "E":  # Выход
                pygame.draw.rect(screen, RED, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
                
    pygame.draw.circle(screen, BLACK, (player_x * tile_size + tile_size // 2, player_y * tile_size + tile_size // 2), tile_size // 3)

# Функция для движения игрока до ближайшего препятствия
def move_player(dx, dy):
    global player_x, player_y, moving

    if moving:
        return  # Если игрок уже двигается, не делаем ничего
    
    moving = True
    target_x = player_x
    target_y = player_y
    
    # Двигаемся до ближайшего препятствия
    while True:
        new_x = target_x + dx
        new_y = target_y + dy
        
        if level_map[new_y][new_x] == "#":  # Стена
            break
        elif level_map[new_y][new_x] == "C":  # Монетка
            level_map[new_y][new_x] = "."  # Монетка собрана
            print("Монетка собрана!")
        
        # Проверяем на выход
        if level_map[new_y][new_x] == "E":
            print("Поздравляем! Вы нашли выход!")
            pygame.quit()
            sys.exit()

        target_x = new_x
        target_y = new_y
    
    # Анимация движения
    move_animation(target_x, target_y)

# Анимация движения игрока
def move_animation(target_x, target_y):
    global player_x, player_y, moving
    
    start_x = player_x
    start_y = player_y
    steps = tile_size // player_speed

    for step in range(steps):
        clock.tick(30)
        player_x = start_x + (target_x - start_x) * (step + 1) / steps
        player_y = start_y + (target_y - start_y) * (step + 1) / steps
        screen.fill(BLACK)
        draw_map()
        pygame.draw.circle(screen, BLACK, (int(player_x * tile_size + tile_size // 2), int(player_y * tile_size + tile_size // 2)), tile_size // 3)
        pygame.display.flip()
    
    # Устанавливаем конечную позицию
    player_x = target_x
    player_y = target_y
    moving = False

# Основной игровой цикл
while True:
    screen.fill(BLACK)
    draw_map()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not moving:
            if event.key == pygame.K_w:  # Вверх
                move_player(0, -1)
            elif event.key == pygame.K_s:  # Вниз
                move_player(0, 1)
            elif event.key == pygame.K_a:  # Влево
                move_player(-1, 0)
            elif event.key == pygame.K_d:  # Вправо
                move_player(1, 0)
