# 🌱💧 Simulador de Manejo de Fertilizantes y Calidad del Agua

> Simulador interactivo (Python + Pygame) para explorar el impacto del manejo agrícola sobre la calidad del agua en zonas rurales.

---

## 🧩 ¿De qué se trata?

Este proyecto es un **simulador educativo** donde el usuario toma decisiones sobre:

- **Cuánto fertilizante aplicar** (bajo, medio, alto)  
- **Cómo manejar las plagas** (manejo integrado vs. uso intensivo de plaguicidas)  
- **Si protege o no el río** con una barrera vegetal

A partir de esas decisiones, el simulador actualiza en cada ciclo:

- La **producción agrícola** (por ciclo y acumulada)  
- La **salud del río** (0–100)  
- El **nivel de contaminación del agua**

El objetivo es lograr un **equilibrio**:  
> Alcanzar un nivel de producción objetivo **sin colapsar el río** 🌍

---

## 🎯 Objetivos del simulador

- Mostrar cómo el uso de **fertilizantes y plaguicidas** afecta la **calidad del agua**.
- Visualizar el **trade-off** entre producción agrícola y conservación ambiental.
- Servir como herramienta de apoyo para:
  - clases sobre **medio ambiente**,  
  - **manejo sostenible de cultivos**,  
  - o problemáticas rurales relacionadas con contaminación de fuentes hídricas.

---

## 🖼️ Interfaz general

Al ejecutar el simulador se ve:

- Un **campo agrícola** y un **río**:
  - El **color del río** cambia según su salud:
    - Azul → río sano  
    - Verde-azulado → en observación  
    - Marrón oscuro → muy deteriorado  

- A la **izquierda**, panel de información:
  - Ciclo actual  
  - Estado del río (SANO / EN OBSERVACIÓN / EN RIESGO ALTO / COLAPSADO)  
  - Nivel de fertilizante  
  - Tipo de manejo de plagas  
  - Existencia de barrera vegetal  
  - Producción del ciclo  
  - Producción acumulada  
  - Objetivo de producción  
  - Salud del río e índice de contaminación  

- Una **barra de salud del río**:
  - Verde → saludable  
  - Amarillo → deterioro  
  - Rojo → en mal estado  

- A la **derecha**, un **panel de botones** para controlar el simulador con el mouse.

> 💡 *(Opcional para el repo)* Aquí puedes añadir un GIF o captura de pantalla:
> `![Captura del simulador](./docs/screenshot.png)`

---

## 🕹️ Mecánica del juego

### Decisiones del usuario

- **Nivel de fertilizante**
  - Bajo → menos producción, menos contaminación  
  - Medio → equilibrio  
  - Alto → mayor producción, mucha más contaminación  

- **Manejo de plagas**
  - Integrado / bajo químico → menor carga de tóxicos  
  - Intensivo químico → mayor carga de tóxicos  

- **Barrera vegetal**
  - Sí → parte de los nutrientes son retenidos antes de llegar al río  
  - No → más nutrientes van directamente al agua  

### Indicadores

- **Producción del ciclo**  
- **Producción acumulada**  
- **Objetivo de producción** (ej: 800 puntos)  
- **Salud del río (0–100)**  
- **Índice de contaminación (0–100)**  

### Condiciones de finalización

- 🟥 **Final “malo” – Río colapsado**
  - Si la salud del río cae por debajo de un umbral (ej: ≤ 10).
  - El simulador se detiene y muestra un mensaje de colapso.

- 🟩 **Final “bueno” – Equilibrio logrado**
  - Si la **producción acumulada** alcanza el objetivo  
  - y la **salud del río** se mantiene por encima de un valor mínimo (ej: > 40).
  - Se muestra un mensaje indicando que lograste producir sin destruir el río.

Además, se muestran **mensajes educativos contextuales**, por ejemplo:

- Reportes de malos olores y peces muertos con alta contaminación.  
- Posibles sanciones ambientales cuando la salud del río es muy baja.  
- Mensajes positivos cuando el manejo es sostenible.

---

## ⌨️ Controles

### Con teclado

| Tecla      | Acción                                       |
|-----------:|----------------------------------------------|
| `1`        | Fertilizante **bajo**                        |
| `2`        | Fertilizante **medio**                       |
| `3`        | Fertilizante **alto**                        |
| `P`        | Cambiar manejo de plagas                     |
| `B`        | Activar / desactivar barrera vegetal         |
| `ESPACIO`  | Avanzar un ciclo                             |
| `R`        | Reiniciar la simulación                      |

### Con mouse (botones)

En el panel derecho:

- **Fertilizante Bajo / Medio / Alto** → cambia el nivel de fertilizante  
- **Cambiar plagas** → alterna entre manejo integrado / intensivo  
- **Barrera Sí/No** → activa o desactiva la barrera vegetal  
- **Avanzar ciclo** → calcula un nuevo ciclo  
- **Reiniciar simulación** → vuelve al estado inicial  

---

## 🏗️ Tecnologías usadas

- [Python](https://www.python.org/)  
- [Pygame](https://www.pygame.org/) para la interfaz gráfica y el bucle del juego  

---

## 📂 Estructura del proyecto

```bash
Simulador/
├── main.py         # Interfaz gráfica, eventos, dibujo y lógica de juego
├── sim_model.py    # Modelo numérico: producción, contaminación y salud del río
└── README.md       # Este archivo
