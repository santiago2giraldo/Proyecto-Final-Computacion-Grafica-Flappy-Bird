import pygame
import random

W, H = 900, 600          # Tamaño de ventana
GRAVEDAD = 2000.0        # Aceleración vertical px/s^2
RESTITUCION = 0.6       # Coeficiente de rebote
ROZAMIENTO_AIRE = 0.5    # Factor por segundo (1 = sin rozamiento)

pygame.init()
screen = pygame.display.set_mode((W, H))
clock  = pygame.time.Clock()
pygame.display.set_caption("Gravedad Pygame")
font = pygame.font.SysFont(None, 22)

def aplicar_gravedad_y_rozamiento(jugador, dt):
    # Rozamiento aplicado como decaimiento exponencial por segundo
    drag = ROZAMIENTO_AIRE ** dt
    jugador["vy"] += GRAVEDAD * dt        # [m/s] = [m/s^2]*[s] ---- v = v_0 +a*t
    jugador ["vx"] *= drag                 
    jugador ["vy"] *= drag     

            
while True:

    dt = clock.tick(120) / 1000.0  # delta tiempo en segundos a 120 FPS máx

    # Entrada de usuario / eventos 
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
