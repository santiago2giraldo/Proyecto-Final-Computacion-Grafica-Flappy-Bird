import pygame
import random
import sys

# ---------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------
W, H = 800, 600
GRAVEDAD = 2000.0
RESTITUCION = 0.6
ROZAMIENTO_AIRE = 0.5

pygame.init()
screen = pygame.display.set_mode((W, H))
clock  = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird - Proyecto")
font = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 26)

# ---------------------------------------
# CONFIGURACIÓN OBSTÁCULOS
# ---------------------------------------
VELOCIDAD_OBSTACULO = 200.0   # Píxeles por segundo
ANCHO_OBSTACULO = 80
ESPACIO_OBSTACULO = 180       # Espacio vertical entre tubos
INTERVALO_OBSTACULO = 1.8     # Segundos entre cada nuevo obstáculo
COLOR_TUBO = (0, 160, 30)     # Un color verde para los tubos

# ---------------------------------------
# FÍSICA DEL JUGADOR
# ---------------------------------------
def aplicar_gravedad_y_rozamiento(jugador, dt):
    drag = ROZAMIENTO_AIRE ** dt
    jugador["vy"] += GRAVEDAD * dt
    jugador["vx"] *= drag
    jugador["vy"] *= drag

# ---------------------------------------
# INSTRUCCIONES
# ---------------------------------------
def instrucciones():
    while True:
        screen.fill((0, 150, 255))

        titulo = font.render("INSTRUCCIONES", True, (255, 255, 255))
        t_rect = titulo.get_rect(center=(W//2, 80))
        screen.blit(titulo, t_rect)

        texto = [
            "Este es el Flappy Bird experimental.",
            "El pájaro cae con gravedad.",
            "Presiona ESPACIO para impulsarte.",
            "",
            "Presiona ESC para volver al menú."
        ]

        y = 160
        for linea in texto:
            r = font_small.render(linea, True, (255,255,255))
            screen.blit(r, (80, y))
            y += 40

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        
        pygame.display.flip()
        clock.tick(60)

# ------------------
# PANTALLA DE INICIO
# -----------------
def pantalla_inicio():
    imagen = pygame.image.load("pantalla_inicio.jpg")
    imagen = pygame.transform.scale(imagen, (W, H))

    start_time = pygame.time.get_ticks()  # tiempo inicial

    while True:
        screen.blit(imagen, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

        if pygame.time.get_ticks() - start_time >= 3000:
            return

        pygame.display.flip()
        clock.tick(60)
# ---------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------
def menu_principal():
    fondo = pygame.image.load("Menu.jpg")
    fondo = pygame.transform.scale(fondo, (W, H))

    # Zonas invisibles donde se puede hacer clic
    # (x, y, width, height)
    boton_jugar = pygame.Rect(W//2 - 150, 240, 300, 70)
    boton_instrucciones = pygame.Rect(W//2 - 150, 320, 300, 70)
    boton_salir = pygame.Rect(W//2 - 150, 400, 300, 70)

    while True:
        screen.blit(fondo, (0, 0))
        mx, my = pygame.mouse.get_pos()

        # --- DEBUG opcional: mostrar contornos ---
        # pygame.draw.rect(screen, (255,0,0), boton_jugar, 2)
        # pygame.draw.rect(screen, (0,255,0), boton_instrucciones, 2)
        # pygame.draw.rect(screen, (0,0,255), boton_salir, 2)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(mx, my):
                    jugar()
                if boton_instrucciones.collidepoint(mx, my):
                    instrucciones()
                if boton_salir.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# --------------------------------
# JUGAR
# --------------------------------
def jugar():

    jugador = {"x": 100, "y": 300, "vx": 0, "vy": 0}
    running = True
    # Lógica de Obstáculos
    # Cada obstáculo será un diccionario: {'x': pos_x, 'centro_y': pos_y_espacio}
    obstaculos = []
    tiempo_para_prox_obstaculo = 1.0 # Empezará a generar inmediatamente

    running = True
    try:
        fondo = pygame.image.load("Fondo.png")
    except Exception as e:
        print("No puedo cargar 'Fondo.png':", e)
        fondo = pygame.Surface((W, H))
        fondo.fill((0, 180, 255))
    fondo = pygame.transform.scale(fondo, (W, H))

    while running:
        dt = clock.tick(120) / 1000.0

        # EVENTOS
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_SPACE:
                    jugador["vy"] = -700  # impulso hacia arriba

        # GENERACIÓN DE OBSTÁCULOS
        tiempo_para_prox_obstaculo -= dt
        if tiempo_para_prox_obstaculo <= 0:
            
            # Reiniciar temporizador
            tiempo_para_prox_obstaculo = INTERVALO_OBSTACULO
            
            # Calcular la posición Y central del espacio
            margen = int(H * 0.25)
            centro_y = random.randint(margen + ESPACIO_OBSTACULO // 2, H - margen - ESPACIO_OBSTACULO // 2)
            
            # Añadir el nuevo obstáculo a la lista
            obstaculos.append({'x': W, 'centro_y': centro_y})
        
        # MOVIMIENTO DE OBSTÁCULOS
        obstaculos_visibles = []
        movimiento_x = VELOCIDAD_OBSTACULO * dt
        
        for obs in obstaculos:
            # Mover el obstáculo hacia la izquierda
            obs['x'] -= movimiento_x
            
            # Mantenerlo en la lista solo si aún es visible
            if obs['x'] + ANCHO_OBSTACULO > 0:
                obstaculos_visibles.append(obs)
                
        obstaculos = obstaculos_visibles

        # FÍSICA
        aplicar_gravedad_y_rozamiento(jugador, dt)

        # POSICIÓN
        jugador["x"] += jugador["vx"] * dt
        jugador["y"] += jugador["vy"] * dt

        # Rebote con el suelo
        if jugador["y"] > H - 40:
            jugador["y"] = H - 40
            jugador["vy"] = -jugador["vy"] * RESTITUCION

        # DIBUJAR
        screen.blit(fondo, (0, 0))
        pygame.draw.circle(screen, (0, 0, 0), (int(jugador["x"]), int(jugador["y"])), 20)
        jugador_img = pygame.image.load("Jugador.png")
        jugador_img = pygame.transform.scale(jugador_img, (98, 98))
        screen.blit(jugador_img, (int(jugador["x"])-46, int(jugador["y"])-53))
        
         
        # DIBUJAR OBSTÁCULOS
        
        for obs in obstaculos:
            x_int = int(obs['x'])
            
            # Calcular rectángulos basados en el centro_y y el espacio
            alto_superior = obs['centro_y'] - ESPACIO_OBSTACULO // 2
            y_inferior = obs['centro_y'] + ESPACIO_OBSTACULO // 2
            alto_inferior = H - y_inferior
            
            # Rectángulo superior
            rect_superior = pygame.Rect(x_int, 0, ANCHO_OBSTACULO, alto_superior)
            pygame.draw.rect(screen, COLOR_TUBO, rect_superior)
            
            # Rectángulo inferior
            rect_inferior = pygame.Rect(x_int, y_inferior, ANCHO_OBSTACULO, alto_inferior)
            pygame.draw.rect(screen, COLOR_TUBO, rect_inferior)
        
        pygame.display.flip()

# ---------------------------------------
# EJECUCIÓN
# ---------------------------------------
pantalla_inicio()
menu_principal()

