import pygame
import sys
from sim_model import calcular_resultados_ciclo

# --- Configuración básica de la ventana ---
ANCHO_VENTANA = 1100
ALTO_VENTANA = 720
FPS = 60  # cuadros por segundo

# --- Colores básicos ---
COLOR_CIELO = (200, 230, 255)
COLOR_CAMPO = (180, 220, 150)

# Colores del río según su salud
COLOR_RIO_SANO = (0, 120, 255)      # azul vivo
COLOR_RIO_MEDIO = (60, 160, 120)    # verde-azulado
COLOR_RIO_MUY_MAL = (80, 60, 40)    # marrón oscuro


def color_rio_por_salud(salud_rio):
    """
    Devuelve un color distinto para el río según la salud.
    Simple: tres rangos (bueno, medio, malo).
    """
    if salud_rio >= 70:
        return COLOR_RIO_SANO
    elif salud_rio >= 40:
        return COLOR_RIO_MEDIO
    else:
        return COLOR_RIO_MUY_MAL


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

    # Simulación activa (no colapsada ni ganada)
    simulacion_activa = True
    simulacion_ganada = False

    # Objetivo de producción (para "ganar" la simulación)
    objetivo_produccion = 5000.0

    # Calculamos resultados del primer ciclo
    produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
        nivel_fertilizante,
        manejo_plagas,
        barrera_vegetal,
        salud_rio
    )

    # Producción total acumulada
    produccion_total = produccion

    # --- Definición de botones (para control con mouse) ---

    # Panel a la derecha de la pantalla
    panel_x = 650
    button_width = ANCHO_VENTANA - panel_x - 40
    button_height = 35
    button_margin = 10

    buttons = []

    # Cada tupla: (texto, acción, valor)
    button_defs = [
        ("Fertilizante Bajo",   "set_fert",        0),
        ("Fertilizante Medio",  "set_fert",        1),
        ("Fertilizante Alto",   "set_fert",        2),
        ("Cambiar plagas",      "toggle_plagas",   None),
        ("Barrera Sí/No",       "toggle_barrera",  None),
        ("Avanzar ciclo",       "step",            None),
        ("Reiniciar simulación","reset",           None),
    ]

    y_btn = 40
    for label, action, value in button_defs:
        rect = pygame.Rect(panel_x, y_btn, button_width, button_height)
        buttons.append({
            "rect": rect,
            "label": label,
            "action": action,
            "value": value,
        })
        y_btn += button_height + button_margin

    ejecutando = True
    while ejecutando:
        # 1. Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            # ---- TECLADO ----
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
                    manejo_plagas = 1 if manejo_plagas == 0 else 0

                # Alternar barrera vegetal
                elif evento.key == pygame.K_b:
                    barrera_vegetal = not barrera_vegetal

                # Avanzar un ciclo
                elif evento.key == pygame.K_SPACE:
                    if simulacion_activa and not simulacion_ganada:
                        ciclo += 1
                        produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
                            nivel_fertilizante,
                            manejo_plagas,
                            barrera_vegetal,
                            salud_rio
                        )
                        produccion_total += produccion

                        # Si el río está muy mal, detener la simulación (final malo)
                        if salud_rio <= 10:
                            simulacion_activa = False
                            simulacion_ganada = False

                        # Si se alcanza el objetivo con el río aceptable, final bueno
                        elif produccion_total >= objetivo_produccion and salud_rio > 40:
                            simulacion_activa = False
                            simulacion_ganada = True

                # Reiniciar simulación
                elif evento.key == pygame.K_r:
                    # Restablecer estado inicial
                    nivel_fertilizante = 1
                    manejo_plagas = 0
                    barrera_vegetal = True
                    salud_rio = 100.0
                    ciclo = 1
                    simulacion_activa = True
                    simulacion_ganada = False
                    produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
                        nivel_fertilizante,
                        manejo_plagas,
                        barrera_vegetal,
                        salud_rio
                    )
                    produccion_total = produccion

            # ---- MOUSE (clic izquierdo) ----
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos

                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        accion = btn["action"]

                        # 1) Cambiar nivel de fertilizante
                        if accion == "set_fert":
                            nivel_fertilizante = btn["value"]

                        # 2) Alternar manejo de plagas
                        elif accion == "toggle_plagas":
                            manejo_plagas = 1 if manejo_plagas == 0 else 0

                        # 3) Alternar barrera vegetal
                        elif accion == "toggle_barrera":
                            barrera_vegetal = not barrera_vegetal

                        # 4) Avanzar un ciclo (igual que con ESPACIO)
                        elif accion == "step":
                            if simulacion_activa and not simulacion_ganada:
                                ciclo += 1
                                produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
                                    nivel_fertilizante,
                                    manejo_plagas,
                                    barrera_vegetal,
                                    salud_rio
                                )
                                produccion_total += produccion

                                if salud_rio <= 10:
                                    simulacion_activa = False
                                    simulacion_ganada = False
                                elif produccion_total >= objetivo_produccion and salud_rio > 40:
                                    simulacion_activa = False
                                    simulacion_ganada = True

                        # 5) Reiniciar simulación (igual que con R)
                        elif accion == "reset":
                            nivel_fertilizante = 1
                            manejo_plagas = 0
                            barrera_vegetal = True
                            salud_rio = 100.0
                            ciclo = 1
                            simulacion_activa = True
                            simulacion_ganada = False
                            produccion, indice_contaminacion, salud_rio = calcular_resultados_ciclo(
                                nivel_fertilizante,
                                manejo_plagas,
                                barrera_vegetal,
                                salud_rio
                            )
                            produccion_total = produccion

        # 2. Lógica adicional del juego (por ahora nada más)

        # 3. Dibujado

        # 3.1. Cielo de fondo
        pantalla.fill(COLOR_CIELO)

        # 3.2. Campo (parte inferior de la pantalla)
        altura_campo = ALTO_VENTANA // 3  # un tercio inferior
        rect_campo = pygame.Rect(
            0,
            ALTO_VENTANA - altura_campo,
            ANCHO_VENTANA,
            altura_campo
        )
        pygame.draw.rect(pantalla, COLOR_CAMPO, rect_campo)

        # 3.3. Río: una franja horizontal que cruza el campo
        altura_rio = 80
        y_rio = ALTO_VENTANA - altura_campo + (altura_campo // 2) - (altura_rio // 2)
        rect_rio = pygame.Rect(0, y_rio, ANCHO_VENTANA, altura_rio)

        color_rio = color_rio_por_salud(salud_rio)
        pygame.draw.rect(pantalla, color_rio, rect_rio)

        # --- Panel de botones (control con mouse) ---

        # Fondo del panel
        panel_rect = pygame.Rect(
            panel_x - 10,
            30,
            button_width + 20,
            (button_height + button_margin) * len(buttons) + 20
        )
        pygame.draw.rect(pantalla, (230, 230, 230), panel_rect)
        pygame.draw.rect(pantalla, (120, 120, 120), panel_rect, 1)

        # Posición actual del mouse (para resaltar botones)
        mouse_pos_actual = pygame.mouse.get_pos()

        for btn in buttons:
            rect = btn["rect"]

            # Si el mouse está encima, cambiamos el color del botón
            if rect.collidepoint(mouse_pos_actual):
                color_btn = (200, 200, 200)
            else:
                color_btn = (240, 240, 240)

            # Dibujar rectángulo del botón
            pygame.draw.rect(pantalla, color_btn, rect)
            pygame.draw.rect(pantalla, (100, 100, 100), rect, 1)

            # Texto centrado en el botón
            label_surface = fuente_peque.render(btn["label"], True, (0, 0, 0))
            label_rect = label_surface.get_rect(center=rect.center)
            pantalla.blit(label_surface, label_rect)

        # --- Construimos los textos explicativos ---

        # Estado cualitativo del río
        if salud_rio >= 70:
            texto_estado_rio = "Estado del río: SANO"
        elif salud_rio >= 40:
            texto_estado_rio = "Estado del río: EN OBSERVACIÓN"
        elif salud_rio > 10:
            texto_estado_rio = "Estado del río: EN RIESGO ALTO"
        else:
            texto_estado_rio = "Estado del río: COLAPSADO"

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
        texto_prod_total = f"Producción acumulada: {produccion_total:.1f} puntos"
        texto_obj = f"Objetivo de producción: {objetivo_produccion:.0f} puntos"
        texto_salud = f"Salud del río: {salud_rio:.1f} / 100"
        texto_cont = f"Índice de contaminación: {indice_contaminacion:.1f} / 100"

        # Controles (texto recordatorio)
        texto_controles_1 = "Teclado: [1] Bajo  [2] Medio  [3] Alto fertilizante"
        texto_controles_2 = "[P] Plagas  |  [B] Barrera  |  [ESPACIO] Ciclo  |  [R] Reiniciar"

        # Mensajes (ganar / perder / educativos)
        if simulacion_ganada:
            texto_mensaje = "¡Lograste el equilibrio! Alcanzaste la producción objetivo sin colapsar el río."
        elif not simulacion_activa and not simulacion_ganada:
            texto_mensaje = "El río ha colapsado. La simulación se ha detenido. Presiona [R] o botón reset."
        else:
            # Mensajes educativos en función del estado actual
            if indice_contaminacion > 60:
                texto_mensaje = "La comunidad río abajo reporta malos olores, color extraño y peces muertos."
            elif salud_rio < 30:
                texto_mensaje = "Las autoridades ambientales evalúan sanciones por la mala calidad del agua."
            elif (indice_contaminacion < 20 and salud_rio > 70
                  and nivel_fertilizante <= 1
                  and manejo_plagas == 0
                  and barrera_vegetal):
                texto_mensaje = "Buen manejo: producción aceptable y el río se mantiene saludable. ¡Sigue así!"
            else:
                texto_mensaje = ""

        # Lista de textos principales
        textos = [
            texto_ciclo,
            texto_estado_rio,
            texto_fert,
            texto_plagas,
            texto_barrera,
            texto_prod,
            texto_prod_total,
            texto_obj,
            texto_salud,
            texto_cont,
        ]

        # Dibujar textos principales
        y = 40
        for t in textos:
            superficie_texto = fuente.render(t, True, (0, 0, 0))  # negro
            pantalla.blit(superficie_texto, (40, y))
            y += 30  # más junto para que quepa todo

        # --- Barra de salud del río ---
        ancho_max_barra = 300
        alto_barra = 20
        x_barra = 40
        y_barra = y + 10  # un poco debajo del último texto

        # Calculamos el ancho según el porcentaje de salud
        ancho_actual = int(ancho_max_barra * (salud_rio / 100.0))

        # Fondo de la barra (contorno gris)
        rect_fondo_barra = pygame.Rect(x_barra, y_barra, ancho_max_barra, alto_barra)
        pygame.draw.rect(pantalla, (80, 80, 80), rect_fondo_barra, 1)  # solo contorno

        # Barra interior (verde si está bien, amarilla/roja si está mal)
        if salud_rio >= 70:
            color_barra = (0, 180, 0)       # verde
        elif salud_rio >= 40:
            color_barra = (200, 180, 0)     # amarillo
        else:
            color_barra = (200, 0, 0)       # rojo

        rect_barra = pygame.Rect(x_barra, y_barra, ancho_actual, alto_barra)
        pygame.draw.rect(pantalla, color_barra, rect_barra)

        # Dibujar los controles en la parte baja
        superficie_controles_1 = fuente_peque.render(texto_controles_1, True, (0, 0, 0))
        superficie_controles_2 = fuente_peque.render(texto_controles_2, True, (0, 0, 0))

        pantalla.blit(superficie_controles_1, (40, ALTO_VENTANA - 70))
        pantalla.blit(superficie_controles_2, (40, ALTO_VENTANA - 45))

        # Mensaje principal (ganar, perder o educativo)
        if texto_mensaje:
            superficie_msg = fuente_peque.render(texto_mensaje, True, (150, 0, 0))
            pantalla.blit(superficie_msg, (40, y_barra + 40))

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()




