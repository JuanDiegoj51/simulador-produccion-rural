# sim_model.py
"""
Módulo con la lógica del simulador:
cálculo de producción, contaminación y salud del río.
"""

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
