import pygame
import sys

# --- Configuración básica ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60  # cuadros por segundo

def main():
    # Inicializar Pygame
    pygame.init()

    # Crear la ventana
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulador - Manejo de fertilizantes y agua")

    reloj = pygame.time.Clock()

    ejecutando = True
    while ejecutando:
        # 1. Manejo de eventos (teclado, ratón, cerrar ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # 2. Lógica del juego (aún vacía, la llenaremos luego)

        # 3. Dibujado en pantalla
        pantalla.fill((200, 230, 255))  # color de fondo (cielo azul clarito)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del bucle
        reloj.tick(FPS)

    # Salir de Pygame de forma ordenada
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
