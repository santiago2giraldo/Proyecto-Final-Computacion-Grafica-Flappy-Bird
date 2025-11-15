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

# ---------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------
def menu_principal():
    fondo = pygame.image.load("menu_flappybird.jpg")
    fondo = pygame.transform.scale(fondo, (W, H))

    # Zonas invisibles donde se puede hacer clic
    # (x, y, width, height)
    boton_jugar = pygame.Rect(W//2 - 100, 210, 400, 70)
    boton_instrucciones = pygame.Rect(W//2 - 100, 300, 400, 70)
    boton_salir = pygame.Rect(W//2 - 100, 380, 400, 70)
    
    while True:
        screen.blit(fondo, (0, 0))
        mx, my = pygame.mouse.get_pos()
        
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
        screen.fill((0, 180, 255))
        pygame.draw.circle(screen, (255, 255, 0), (int(jugador["x"]), int(jugador["y"])), 20)

        pygame.display.flip()
# ---------------------------------------
# EJECUCIÓN
# ---------------------------------------
menu_principal()

