import pygame
import sys

# --- Configuración básica de la ventana ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60  # cuadros por segundo

# --- Modelo numérico simplificado ---

def calcular_resultados_ciclo(nivel_fertilizante, manejo_plagas, barrera_vegetal, salud_rio_anterior):
    """
    Calcula producción, contaminación y nueva salud del río,
    según las decisiones del jugador y la salud anterior.
    """

    # Producción base según nivel de fertilizante
    produccion_base_por_fertilizante = {
        0: 40,  # bajo
        1: 70,  # medio
        2: 85,  # alto
    }

    # Carga de nutrientes que se pierden al agua según fertilizante (antes de barrera)
    carga_nutrientes_por_fertilizante = {
        0: 10,  # bajo
        1: 25,  # medio
        2: 45,  # alto
    }

    # 1) Producción del ciclo
    produccion = produccion_base_por_fertilizante[nivel_fertilizante]

    # 2) Carga de nutrientes al agua
    carga_nutrientes = carga_nutrientes_por_fertilizante[nivel_fertilizante]

    # Si hay barrera vegetal, reduce la carga de nutrientes en un 60%
    if barrera_vegetal:
        carga_nutrientes_final = carga_nutrientes * 0.4
    else:
        carga_nutrientes_final = carga_nutrientes

    # 3) Carga de tóxicos según manejo de plagas
    if manejo_plagas == 0:  # manejo integrado / bajo químico
        carga_toxicos = 5
    else:  # intensivo químico
        carga_toxicos = 25

    # 4) Índice de contaminación del ciclo (muy simplificado)
    indice_contaminacion = min(100, carga_nutrientes_final + carga_toxicos)

    # 5) Actualizar salud del río
    impacto_salud = (carga_nutrientes_final / 10.0) + (carga_toxicos / 5.0)
    salud_rio = salud_rio_anterior - impacto_salud + 3.0  # +3 por recuperación natural

    # Limitar entre 0 y 100
    if salud_rio < 0:
        salud_rio = 0
    if salud_rio > 100:
        salud_rio = 100

    return produccion, indice_contaminacion, salud_rio


def main():
    # Inicializar Pygame
    pygame.init()

    # Crear ventana
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulador - Manejo de fertilizantes y agua")

    reloj = pygame.time.Clock()

    # Fuente para mostrar texto
    fuente = pygame.font.SysFont(None, 28)
    fuente_peque = pygame.font.SysFont(None, 22)

    # --- Estado inicial del modelo ---

    # Decisiones del jugador (valores iniciales)
    nivel_fertilizante = 1      # 0 = bajo, 1 = medio, 2 = alto
    manejo_plagas = 0           # 0 = integrado, 1 = intensivo
    barrera_vegetal = True      # True = hay barrera, False = no hay

    # Salud inicial del río
    salud_rio = 100.0

    # Ciclo actual
    ciclo = 1

    # Calculamos resultados del primer ciclo
    produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
        nivel_fertilizante,
        manejo_plagas,
        barrera_vegetal,
        salud_rio
    )

    ejecutando = True
    while ejecutando:
        # 1. Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                # Cambiar nivel de fertilizante
                if evento.key == pygame.K_1:
                    nivel_fertilizante = 0  # bajo
                elif evento.key == pygame.K_2:
                    nivel_fertilizante = 1  # medio
                elif evento.key == pygame.K_3:
                    nivel_fertilizante = 2  # alto

                # Alternar manejo de plagas
                elif evento.key == pygame.K_p:
                    if manejo_plagas == 0:
                        manejo_plagas = 1
                    else:
                        manejo_plagas = 0

                # Alternar barrera vegetal
                elif evento.key == pygame.K_b:
                    barrera_vegetal = not barrera_vegetal

                # Avanzar un ciclo
                elif evento.key == pygame.K_SPACE:
                    ciclo += 1
                    produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
                        nivel_fertilizante,
                        manejo_plagas,
                        barrera_vegetal,
                        salud_rio
                    )

        # 2. Lógica adicional del juego (por ahora nada más)

        # 3. Dibujado
        pantalla.fill((200, 230, 255))  # fondo azul claro

        # --- Construimos los textos explicativos ---

        # Texto del ciclo actual
        texto_ciclo = f"Ciclo actual: {ciclo}"

        # Texto del nivel de fertilizante
        if nivel_fertilizante == 0:
            texto_fert = "Fertilizante: Bajo (menos producción, menos contaminación)"
        elif nivel_fertilizante == 1:
            texto_fert = "Fertilizante: Medio (equilibrio)"
        else:
            texto_fert = "Fertilizante: Alto (más producción, más contaminación)"

        # Texto del manejo de plagas
        if manejo_plagas == 0:
            texto_plagas = "Manejo de plagas: Integrado / bajo químico"
        else:
            texto_plagas = "Manejo de plagas: Intensivo químico"

        # Texto de barrera vegetal
        texto_barrera = "Barrera vegetal junto al río: Sí" if barrera_vegetal else "Barrera vegetal junto al río: No"

        # Resultados numéricos
        texto_prod = f"Producción del ciclo: {produccion:.1f} puntos"
        texto_salud = f"Salud del río: {salud_rio:.1f} / 100"
        texto_cont = f"Índice de contaminación: {indice_contaminacion:.1f} / 100"

        # Controles
        texto_controles_1 = "Controles: [1] Bajo  [2] Medio  [3] Alto fertilizante"
        texto_controles_2 = "[P] Cambiar manejo de plagas  |  [B] Barrera vegetal Sí/No  |  [ESPACIO] Avanzar ciclo"

        # Lista de textos principales
        textos = [
            texto_ciclo,
            texto_fert,
            texto_plagas,
            texto_barrera,
            texto_prod,
            texto_salud,
            texto_cont,
        ]

        # Dibujar textos principales
        y = 40
        for t in textos:
            superficie_texto = fuente.render(t, True, (0, 0, 0))  # negro
            pantalla.blit(superficie_texto, (40, y))
            y += 40

        # Dibujar los controles en la parte baja
        superficie_controles_1 = fuente_peque.render(texto_controles_1, True, (0, 0, 0))
        superficie_controles_2 = fuente_peque.render(texto_controles_2, True, (0, 0, 0))

        pantalla.blit(superficie_controles_1, (40, ALTO_VENTANA - 70))
        pantalla.blit(superficie_controles_2, (40, ALTO_VENTANA - 45))

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

