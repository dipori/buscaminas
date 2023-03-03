# se improtan las librerias
import pygame
import random
import sys

# Configuración del juego
NUM_FILAS = 9
NUM_COLS = 9
CELL_SIZE = 40
SCREEN_WIDTH = CELL_SIZE * NUM_COLS
SCREEN_HEIGHT = CELL_SIZE * NUM_FILAS
PROP_MINAS = 0.1
GRIS = (192, 192, 192)
NEGRO = (0, 0, 0)
final_partida = False

# Inicializa el tablero
def init_tablero():
    global tablero, num_minas, mostrado
    num_minas = int(NUM_FILAS * NUM_COLS * PROP_MINAS)
    tablero = [[0 for x in range(NUM_COLS)] for y in range(NUM_FILAS)]
    for i in range(num_minas):
        x = random.randint(0, NUM_COLS - 1)
        y = random.randint(0, NUM_FILAS - 1)
        while tablero[y][x] == -1:
            x = random.randint(0, NUM_COLS - 1)
            y = random.randint(0, NUM_FILAS - 1)
        tablero[y][x] = -1
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if (dx != 0 or dy != 0) and (x + dx >= 0 and x + dx < NUM_COLS and y + dy >= 0 and y + dy < NUM_FILAS) and (tablero[y+dy][x+dx] != -1):
                    tablero[y+dy][x+dx] += 1
    mostrado = [[False for x in range(NUM_COLS)] for y in range(NUM_FILAS)]

# Función para actualizar la pantalla
def update_screen():
    for y in range(NUM_FILAS):
        for x in range(NUM_COLS):
            if mostrado[y][x]:
                if tablero[y][x] == -1:
                    pygame.draw.rect(screen, NEGRO, (x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-1, CELL_SIZE-1))
                else:
                    pygame.draw.rect(screen, GRIS, (x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-1, CELL_SIZE-1))
                    # Mostrar número de minas adyacentes
                    font = pygame.font.Font(None, int(CELL_SIZE*0.8))
                    text = font.render(str(tablero[y][x]), True, NEGRO)
                    text_rect = text.get_rect(center=(x*CELL_SIZE+CELL_SIZE/2, y*CELL_SIZE+CELL_SIZE/2))
                    screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRIS, (x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-1, CELL_SIZE-1))
    pygame.display.flip()



def muestra(x, y):
    global final_partida

    if tablero[y][x] == -1:
        print("¡Mina encontrada! ¡Perdiste!")
        final_partida = True
    else:
        mostrado[y][x] = True
        if tablero[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (dx != 0 or dy != 0) and (x + dx >= 0 and x + dx < NUM_COLS and y + dy >= 0 and y + dy < NUM_FILAS) and (not mostrado[y+dy][x+dx]):
                        muestra(x+dx, y+dy)



# Definir función principal

# Inicializa Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Buscaminas")


init_tablero()

# Bucle principal del juego
while not final_partida:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            final_partida = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x = pos[0] // CELL_SIZE
            y = pos[1] // CELL_SIZE
            if event.button == 1:  # Click izquierdo
                muestra(x, y)
            elif event.button == 3:  # Click derecho
                mostrado[y][x] = not mostrado[y][x]
    update_screen()


    # Verificar si el juego ha terminado
    if not any(False in row for row in mostrado):
        
        pygame.draw.rect(screen, NEGRO, (1, 1, SCREEN_WIDTH-1, SCREEN_HEIGHT-1))
                
        font = pygame.font.Font(None, 36)
        text = font.render('¡Ganaste!', True, (255, 255, 255))
        
        text_rect = text.get_rect()
        text_rect.center = screen.get_rect().center
        
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        final_partida = True

    elif final_partida:
        
        pygame.draw.rect(screen, NEGRO, (1, 1, SCREEN_WIDTH-1, SCREEN_HEIGHT-1))
        
        font = pygame.font.Font(None, 36)
        text = font.render('¡Mina encontrada! ¡Perdiste!', True, (255, 255, 255))
        
        text_rect = text.get_rect()
        text_rect.center = screen.get_rect().center
        
        screen.blit(text, text_rect)
        
        pygame.display.flip()

while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()



