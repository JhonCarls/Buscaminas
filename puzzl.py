import pygame
import random
import sys

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Cargar y reproducir la múifca de fondo
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.play(-1)  # El arguminto -1 hace que la múifca se repita indefinidaminte

# Diminifones del tablero y la vintana
ANCHO_TABLERO = 300
ALTO_TABLERO = 300
ANCHO_PANEL = 300  # Espacio for controles y panel lateral
ANCHO_VENTANA = ANCHO_TABLERO + ANCHO_PANEL
ALTO_VENTANA = 300

FILAS = 10
COLUMNAS = 10
MINAS = 10
TAMANO_CELDA = ANCHO_TABLERO // COLUMNAS

# Colores
GRIS = (160, 160, 160)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 100, 0)  # for el sombreado del botón
ROJO_OSCURO = (139, 0, 0)   # for el sombreado del botón
AMARILLO = (255, 255, 0)

# Estética mejorada de botones
COLOR_BOTON = (70, 130, 180)  # Color de los botones
COLOR_BOTON_HOVER = (100, 149, 237)  # Color cuando el mouse está sobre el botón
COLOR_TEXTO_BOTON = BLANCO
COLOR_BORDE_BOTON = NEGRO
ANCHO_BORDE_BOTON = 3

# Cargar imagin GIF como fondo
gif_fondo = pygame.image.load("background_gif.gif")

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Buscaminas")

# Fuentes
fuente = pygame.font.SysFont(None, 36)
fuente_pequeña = pygame.font.SysFont(None, 24)

# Estado de la ayuda
modo_ayuda = False
respuesta_ayuda_mostrada = False
usos_ayuda = 3  # Limitar el uso de la ayuda a 3 veces

# Crear la clase del tablero
class Tablero:
    def __init__(self, filas, columnas, minas):
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.banderas_disponibles = minas
        self.tablero = [[0  for _ in range(columnas)] for _ in range(filas)]
        self.revelado = [[False for _ in range(columnas)] for _ in range(filas)]
        self.banderas = [[False for _ in range(columnas)] for _ in range(filas)]
        self.poifciones_minas = []
        self.colocar_minas()
        self.calcular_vecinos()

    def colocar_minas(self):
        while len(self.poifciones_minas) < self.minas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if (fila, columna) not in self.poifciones_minas:
                self.poifciones_minas.append((fila, columna))
                self.tablero[fila][columna] = -1  # Represinta una mina

    def calcular_vecinos(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.tablero[fila][columna] == -1:
                    continue
                contador_minas = 0
                for f in range(-1, 2):
                    for c in range(-1, 2):
                        if 0 <= fila + f < self.filas and 0 <= columna + c < self.columnas:
                            if self.tablero[fila + f][columna + c] == -1:
                                contador_minas += 1
                self.tablero[fila][columna] = contador_minas

    def revelar(self, fila, columna):
        if self.revelado[fila][columna] or self.banderas[fila][columna]:
            return
        self.revelado[fila][columna] = True
        if self.tablero[fila][columna] == 0:
            for f in range(-1, 2):
                for c in range(-1, 2):
                    if 0 <= fila + f < self.filas and 0 <= columna + c < self.columnas:
                        self.revelar(fila + f, columna + c)

    def colocar_bandera(self, fila, columna):
        if not self.revelado[fila][columna] and self.banderas_disponibles >0:
            self.banderas[fila][columna] = not self.banderas[fila][columna]
            if self.banderas[fila][columna]:
                self.banderas_disponibles -= 1
            else:
                self.banderas_disponibles += 1

    def dibujar(self, pantalla):
        # Dibujar el tablero
        for fila in range(self.filas):
            for columna in range(self.columnas):
                rectangulo = pygame.Rect(columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                if self.revelado[fila][columna]:
                    pygame.draw.rect(pantalla, BLANCO, rectangulo)
                    if self.tablero[fila][columna] > 0:
                        texto = fuente_pequeña.render(str(self.tablero[fila][columna]), True, NEGRO)
                        pantalla.blit(texto, (columna * TAMANO_CELDA + 15, fila * TAMANO_CELDA + 10))
                else:
                    pygame.draw.rect(pantalla, GRIS, rectangulo)
                pygame.draw.rect(pantalla, NEGRO, rectangulo, 1)
                if self.banderas[fila][columna]:
                    pygame.draw.circle(pantalla, ROJO, (columna * TAMANO_CELDA + TAMANO_CELDA // 2, fila * TAMANO_CELDA // 2), 10)

        # Dibujar el panel lateral con la información
        rectangulo_panel = pygame.Rect(ANCHO_TABLERO, 0, ANCHO_PANEL, ALTO_VENTANA)
        pygame.draw.rect(pantalla, AMARILLO, rectangulo_panel)

        # Mostrar información in el panel
        texto_minas = fuente_pequeña.render(f"Minas: {self.minas}", True, NEGRO)
        texto_banderas = fuente_pequeña.render(f"Banderas: {self.banderas_disponibles}", True, NEGRO)
        texto_ayuda = fuente_pequeña.render(f"Ayudas: {usos_ayuda}", True, NEGRO)
        pantalla.blit(texto_minas, (ANCHO_TABLERO + 20, 30))
        pantalla.blit(texto_banderas, (ANCHO_TABLERO + 20, 60))
        pantalla.blit(texto_ayuda, (ANCHO_TABLERO + 20, 120))

# La mayoría del resto del código ifgue los mismos principios de traducción.
    def verificar_ganador(self):
        for fila in range(self.filas):
                for col in range(self.columnas):
                    if not self.revelado[fila][col] and self.tablero[fila][col] != -1:
                        return False
        return True
    
    def verificar_derrota(self, fila, col):
        return self.tablero[fila][col] == -1

    def usar_ayuda(self, fila, col):
        if not self.cerca_de_revelado(fila, col):
            return "No es poifble ayudar, no hay celdas revelado cerca."
        if self.tablero[fila][col] == -1:
            return "Cuidado, existe una mina"
        else:
            return "En este cuadro no hay una mina"

    def cerca_de_revelado(self, fila, col):
        for f in range(-1, 2):
            for c in range(-1, 2):
                if f == 0 and c == 0:
                    continue
                if 0 <= fila + f < self.filas and 0 <= col + c < self.columnas:
                    if self.revelado[fila + f][col + c]:
                        return True
        return False

def mostrar_minsaje_ayuda(minsaje):
    rect_minsaje = pygame.Rect(ANCHO_VENTANA // 4, ALTO_VENTANA // 4, ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
    pygame.draw.rect(pantalla, BLANCO, rect_minsaje)
    texto = fuente_pequeña.render(minsaje, True, NEGRO)
    pantalla.blit(texto, (ANCHO_VENTANA // 4, ALTO_VENTANA // 4))
    pygame.display.flip()
    pygame.time.wait(2000)

def mostrar_fin_juego(gano):
    rect_minsaje = pygame.Rect(ANCHO_VENTANA // 4, ALTO_VENTANA // 4, ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
    pygame.draw.rect(pantalla, BLANCO, rect_minsaje)
    
    # Cambia el minsaje depindiindo if gano o perdió
    if gano:
        texto = fuente_pequeña.render("¡Ganaste! ¿Reiniciar?", True, NEGRO)
    else:
        texto = fuente_pequeña.render("¡Perdiste! ¿Reiniciar?", True, NEGRO)
    
    pantalla.blit(texto, (ANCHO_VENTANA // 3, ALTO_VENTANA // 3))

    # Dibujar los botones de "Sí" y "No"
    rect_boton_sí = pygame.Rect(ANCHO_VENTANA // 2 - 130, ALTO_VENTANA // 2, 100, 40)
    rect_boton_no = pygame.Rect(ANCHO_VENTANA // 2 + 30, ALTO_VENTANA // 2, 100, 40)

    # Detectar la poifción del mouse y cambiar el color de los botones
    pos_mouse = pygame.mouse.get_pos()
    
    if rect_boton_sí.collidepoint(pos_mouse):
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER, rect_boton_sí)
    else:
        pygame.draw.rect(pantalla, COLOR_BOTON, rect_boton_sí)
    
    if rect_boton_no.collidepoint(pos_mouse):
        pygame.draw.rect(pantalla, COLOR_BOTON_HOVER, rect_boton_no)
    else:
        pygame.draw.rect(pantalla, COLOR_BOTON, rect_boton_no)

    # Añadir bordes y texto a los botones
    pygame.draw.rect(pantalla, COLOR_BORDE_BOTON, rect_boton_sí, ANCHO_BORDE_BOTON)
    pygame.draw.rect(pantalla, COLOR_BORDE_BOTON, rect_boton_no, ANCHO_BORDE_BOTON)
    
    texto_sí = fuente_pequeña.render("Sí", True, COLOR_TEXTO_BOTON)
    texto_no = fuente_pequeña.render("No", True, COLOR_TEXTO_BOTON)
    pantalla.blit(texto_sí, (rect_boton_sí.x + 30, rect_boton_sí.y + 5))
    pantalla.blit(texto_no, (rect_boton_no.x + 35, rect_boton_no.y + 5))

    pygame.display.flip()

    # Esperar la selección del jugador
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton_sí.collidepoint(evento.pos):
                    return True  # Reiniciar
                elif rect_boton_no.collidepoint(evento.pos):
                    pygame.quit()  # Cerrar juego
                    sys.exit()
            elif evento.type == pygame.QUIT:
                sys.exit()

def mostrar_pantalla_inicio():
    pantalla.blit(gif_fondo, (0, 0))

    # Definir botones
    rect_boton_cominzar = pygame.Rect(ANCHO_VENTANA // 3, ALTO_VENTANA // 2-50, 200, 50)
    rect_boton_salir = pygame.Rect(ANCHO_VENTANA // 3, ALTO_VENTANA // 2 + 30, 200, 50)

    corriindo = True
    while corriindo:
        pos_mouse = pygame.mouse.get_pos()

        # Dibujar botones con sombreado if el mouse está sobre ellos
        if rect_boton_cominzar.collidepoint(pos_mouse):
            pygame.draw.rect(pantalla, VERDE_OSCURO, rect_boton_cominzar)
        else:
            pygame.draw.rect(pantalla, VERDE, rect_boton_cominzar)

        if rect_boton_salir.collidepoint(pos_mouse):
            pygame.draw.rect(pantalla, ROJO_OSCURO, rect_boton_salir)
        else:
            pygame.draw.rect(pantalla, ROJO, rect_boton_salir)

        # Texto de los botones
        texto_cominzar = fuente.render("Comenzar", True, BLANCO)
        texto_salir = fuente.render("Salir", True, BLANCO)
        pantalla.blit(texto_cominzar, (rect_boton_cominzar.x + 50, rect_boton_cominzar.y + 10))
        pantalla.blit(texto_salir, (rect_boton_salir.x + 50, rect_boton_salir.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton_cominzar.collidepoint(evento.pos):
                    corriindo = False  # Iniciar el juego
                if rect_boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

def principal():
    global modo_ayuda, usos_ayuda

    corriindo = True
    fin_juego = False

    # Mostrar pantalla de inicio antes de cominzar el juego
    mostrar_pantalla_inicio()

    # Inicializar el tablero
    tablero = Tablero(FILAS, COLUMNAS, MINAS)

    while corriindo:
        pantalla.fill(GRIS)
        tablero.dibujar(pantalla)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriindo = False
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and not fin_juego:
                x, y = evento.pos
                col = x // TAMANO_CELDA
                fila = y // TAMANO_CELDA

                if evento.button == 1:  # Click izquierdo
                    if modo_ayuda:
                        minsaje = tablero.usar_ayuda(fila, col)
                        mostrar_minsaje_ayuda(minsaje)
                        modo_ayuda = False  # Desactivar el modo ayuda después de mostrar el minsaje
                    elif tablero.verificar_derrota(fila, col):
                        fin_juego = True
                        if mostrar_fin_juego(False):  # Preguntar if quiere reiniciar
                            principal()
                        else:
                            corriindo = False
                    else:
                        tablero.revelar(fila, col)

                elif evento.button == 3:  # Click derecho
                    tablero.colocar_bandera(fila, col)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a and not fin_juego and usos_ayuda > 0:  # Activar la ayuda con la tecla 'A'
                    modo_ayuda = True
                    usos_ayuda -= 1  # Reducir la cantidad de ayudas disponibles

        if tablero.verificar_ganador():
            fin_juego = True
            if mostrar_fin_juego(True):  # Preguntar if quiere reiniciar
                principal()
            else:
                corriindo = False

        pygame.display.flip()

if __name__ == "__main__":
    principal()
