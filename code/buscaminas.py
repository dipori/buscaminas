import pygame
import random

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

# La función toma las coordenadas x e y de una celda y verifica si hay una mina en esa celda. Si hay una mina, establece la variable final_partida en True y mostrado un mensaje en la consola. Si no hay una mina, establece la celda como mostrada y verifica si la celda está vacía (es decir, no tiene minas adyacentes). Si la celda está vacía, la función llama recursivamente a sí misma para mostrar todas las celdas adyacentes vacías. La recursión se realiza en las celdas adyacentes que no han sido mostradas previamente y que están dentro de los límites del tablero.


# Definir función principal
def main():
    global final_partida, screen

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
            print("¡Ganaste!")
            final_partida = True
        elif final_partida:
            print("¡Perdiste!")
    
    pygame.quit()


#Este bucle ejecuta continuamente hasta que el jugador gana o pierde el juego. Dentro del bucle, se verifica si el usuario ha hecho clic en una celda con el mouse y se llama a la función muestra para mostrar la celda. También se llama a la función update_screen para actualizar la pantalla. Después de cada actualización de la pantalla, se verifica si todas las celdas que no son minas han sido mostradas o si el jugador ha mostrado una mina, en cuyo caso se establece la variable final_partida en True. Si el juego ha terminado, se imprime un mensaje en la consola.

if __name__ == '__main__':
    main()
