import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
width = 400
height = 400
cell_size = 40
rows = height // cell_size
cols = width // cell_size

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Configuración de la ventana
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Buscaminas")

# Crear el tablero
board = [[{'mine': False, 'revealed': False, 'count': 0} for _ in range(cols)] for _ in range(rows)]

# Colocar minas
num_mines = 10
mines = set()
while len(mines) < num_mines:
    mines.add((random.randrange(rows), random.randrange(cols)))

for mine in mines:
    board[mine[0]][mine[1]]['mine'] = True

# Calcular números alrededor de las minas
for i in range(rows):
    for j in range(cols):
        if not board[i][j]['mine']:
            count = 0
            for x in range(max(0, i-1), min(rows, i+2)):
                for y in range(max(0, j-1), min(cols, j+2)):
                    if board[x][y]['mine']:
                        count += 1
            board[i][j]['count'] = count

# Función para revelar una casilla
def reveal(x, y):
    if 0 <= x < rows and 0 <= y < cols and not board[x][y]['revealed']:
        board[x][y]['revealed'] = True
        if board[x][y]['count'] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    reveal(x + dx, y + dy)

# Bucle principal del juego
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row = y // cell_size
            col = x // cell_size
            if board[row][col]['mine']:
                game_over = True
            else:
                reveal(row, col)

    screen.fill(BLACK)
    
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            if board[i][j]['revealed']:
                if board[i][j]['mine']:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if board[i][j]['count'] > 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(board[i][j]['count']), True, BLACK)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, WHITE, rect, 1)

    pygame.display.flip()

pygame.quit()