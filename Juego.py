import pygame
import random
import sys
import cv2
import mediapipe as mp
import numpy as np  

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
VELOCIDAD_OBSTACULO = 200.0
ANCHO_OBSTACULO = 80
ESPACIO_OBSTACULO = 180
INTERVALO_OBSTACULO = 1.8
COLOR_TUBO = (0, 160, 30)

# ---------------------------------------
# CARGA DE RECURSOS
# ---------------------------------------
try:
    jugador_img = pygame.image.load("Jugador.png")
    jugador_img = pygame.transform.scale(jugador_img, (98, 98))
    img_tuberia_orig = pygame.image.load("Tuberias.png")
    tuberia_abajo = pygame.transform.scale(img_tuberia_orig, (ANCHO_OBSTACULO, H))
    tuberia_arriba = pygame.transform.flip(tuberia_abajo, False, True)
except:
    tuberia_abajo = pygame.Surface((ANCHO_OBSTACULO, H))
    tuberia_abajo.fill(COLOR_TUBO)
    tuberia_arriba = tuberia_abajo

# ----- Sonidos -----
try:
    sonido_salto = pygame.mixer.Sound("sonido_pasar_obstaculo.mp3")
    sonido_colision = pygame.mixer.Sound("sonido_colision.mp3")
except:
    sonido_salto = None
    sonido_colision = None

# ---------------------------------------
# FÍSICA
# ---------------------------------------
def aplicar_gravedad_y_rozamiento(jugador, dt):
    drag = ROZAMIENTO_AIRE ** dt
    jugador["vy"] += GRAVEDAD * dt
    jugador["vx"] *= drag
    jugador["vy"] *= drag

# ---------------------------------------
# USO DE LA CÁMARA
# ---------------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
# ---------------------------------------
# INSTRUCCIONES
# ---------------------------------------
def instrucciones():
    while True:
        instrucciones_img = pygame.image.load("instrucciones.png")
        instrucciones_img = pygame.transform.scale(instrucciones_img, (W, H))
        screen.blit(instrucciones_img, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        
        pygame.display.flip()
        clock.tick(60)

# ---------------------------------------
# PANTALLA DE INICIO
# ---------------------------------------
def pantalla_inicio():
    imagen = pygame.image.load("pantalla_inicio.jpg")
    imagen = pygame.transform.scale(imagen, (W, H))

    start_time = pygame.time.get_ticks()

    while True:
        screen.blit(imagen, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
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

    boton_jugar = pygame.Rect(W//2 - 150, 240, 300, 70)
    boton_instrucciones = pygame.Rect(W//2 - 150, 320, 300, 70)
    boton_salir = pygame.Rect(W//2 - 150, 400, 300, 70)

    while True:
        screen.blit(fondo, (0, 0))
        mx, my = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(mx, my):
                    jugar()
                if boton_instrucciones.collidepoint(mx, my):
                    instrucciones()
                if boton_salir.collidepoint(mx, my):
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# ---------------------------------------
# JUEGO PRINCIPAL
# ---------------------------------------
def jugar():

    jugador = {"x": 100, "y": 300, "vx": 0, "vy": 0}

    # Obstáculos
    obstaculos = []
    tiempo_para_prox_obstaculo = 1.0

    # Puntaje
    puntaje = 0

    # Cargar fondo
    try:
        fondo = pygame.image.load("Fondo.png")
    except:
        fondo = pygame.Surface((W, H))
        fondo.fill((0, 180, 255))
    fondo = pygame.transform.scale(fondo, (W, H))

    running = True

    while running:
        dt = clock.tick(120) / 1000.0
# ---------------------------------------
# Uso de la cámara
# ---------------------------------------
        ret, frame = cap.read()
        if not ret:
            continue

        # Voltear el frame horizontalmente para una vista tipo espejo
        frame = cv2.flip(frame, 1)
    
        # Convertir la imagen a RGB (MediaPipe requiere RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Procesar el frame para detectar manos
        results = hands.process(rgb_frame)
        # Si se detectan manos
        if results.multi_hand_landmarks:
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Obtener las coordenadas de los dedos pulgar e índice
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

            # Calcular la distancia entre los dedos
            distance = np.sqrt(
                (thumb_tip.x - index_tip.x)**2 + 
                (thumb_tip.y - index_tip.y)**2
            )

        # EVENTOS
        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_SPACE:
                    jugador["vy"] = -700

        # GENERAR OBSTÁCULOS
        tiempo_para_prox_obstaculo -= dt
        if tiempo_para_prox_obstaculo <= 0:
            tiempo_para_prox_obstaculo = INTERVALO_OBSTACULO
            margen = int(H * 0.25)
            centro_y = random.randint(margen + ESPACIO_OBSTACULO // 2,
                                      H - margen - ESPACIO_OBSTACULO // 2)
            obstaculos.append({"x": W, "centro_y": centro_y, "contado": False})

        # MOVER OBSTÁCULOS
        obstaculos_nuevos = []
        mov_x = VELOCIDAD_OBSTACULO * dt
        for obs in obstaculos:
            obs["x"] -= mov_x
            if obs["x"] + ANCHO_OBSTACULO > 0:
                obstaculos_nuevos.append(obs)
        obstaculos = obstaculos_nuevos

        # FÍSICA
        aplicar_gravedad_y_rozamiento(jugador, dt)
        jugador["y"] += jugador["vy"] * dt

        # --- COLISIÓN ARRIBA/ABAJO ---
        if jugador["y"] < 0:
            jugador["y"] = 0
            running = False

        if jugador["y"] > H - 40:
            jugador["y"] = H - 40
            running = False

        # --- COLISIÓN CON TUBERÍAS ---
        for obs in obstaculos:
            x = int(obs["x"])
            alto_sup = obs["centro_y"] - ESPACIO_OBSTACULO // 2
            y_inf = obs["centro_y"] + ESPACIO_OBSTACULO // 2

            # Puntaje (solo una vez por obstáculo)
            if not obs["contado"] and x + ANCHO_OBSTACULO < jugador["x"]:
                puntaje += 1
                obs["contado"] = True
                if sonido_salto: sonido_salto.play()

            # Colisión
            if (x < jugador["x"] < x + ANCHO_OBSTACULO):
                if jugador["y"] < alto_sup or jugador["y"] > y_inf:
                    running = False

        # DIBUJAR
        screen.blit(fondo, (0, 0))
        screen.blit(jugador_img, (int(jugador["x"])-46, int(jugador["y"])-53))

        # Dibujar tubos
        for obs in obstaculos:
            x = int(obs["x"])
            alto_sup = obs["centro_y"] - ESPACIO_OBSTACULO // 2
            y_inf = obs["centro_y"] + ESPACIO_OBSTACULO // 2

            screen.blit(tuberia_arriba, (x, alto_sup - H))
            screen.blit(tuberia_abajo, (x, y_inf))

        # Puntaje
        txt = font.render(f"Puntaje: {puntaje}", True, (255,255,255))
        screen.blit(txt, (20, 20))
        

        pygame.display.flip()

    # ---------------------------------------------------
    # GAME OVER
    # ---------------------------------------------------
    if sonido_colision: sonido_colision.play()

    while True:
        screen.blit(fondo, (0,0))

        game_over = font.render("GAME OVER", True, (255,0,0))
        screen.blit(game_over, game_over.get_rect(center=(W//2, H//2 - 50)))

        puntaje_final = font_small.render(f"Puntaje: {puntaje}", True, (0,0,0))
        screen.blit(puntaje_final, puntaje_final.get_rect(center=(W//2, H//2 + 10)))

        presiona = font_small.render("Presiona cualquier tecla...", True, (0,0,0))
        screen.blit(presiona, presiona.get_rect(center=(W//2, H//2 + 60)))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                return

# ---------------------------------------
# EJECUCIÓN
# ---------------------------------------
pantalla_inicio()
menu_principal()
