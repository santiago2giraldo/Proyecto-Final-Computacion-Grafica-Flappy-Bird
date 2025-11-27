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
try:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
except Exception as e:
    print("Warning: MediaPipe no pudo inicializarse:", e)
    hands = None
    mp_draw = None

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Warning: no se pudo abrir la cámara (cap).")
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
    # ...existing code...
    # Obstáculos
    obstaculos = []
    tiempo_para_prox_obstaculo = INTERVALO_OBSTACULO
# ...existing code...
    # --- Esperar a que el jugador esté listo antes de empezar ---
    started = False
    PINCH_THRESHOLD = 0.04

    while not started:
        dt = clock.tick(30) / 1000.0

        # leer cámara y crear preview (igual que en el bucle principal)
        ret, frame = cap.read()
        cam_preview = None
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if hands is not None:
                results = hands.process(rgb_frame)
            else:
                results = None
            try:
                cam_surf = pygame.image.frombuffer(rgb_frame.tobytes(), (frame.shape[1], frame.shape[0]), 'RGB')
                cam_preview = pygame.transform.scale(cam_surf, (320, 240))
            except:
                cam_preview = None

        # eventos para iniciar
        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_RETURN):
                started = True
            if e.type == pygame.MOUSEBUTTONDOWN:
                started = True

        # dibujar pantalla LISTO
        screen.blit(fondo, (0, 0))
        screen.blit(jugador_img, (int(jugador["x"]) - 46, int(jugador["y"]) - 53))
        if cam_preview is not None:
            screen.blit(cam_preview, (W - 320 - 10, 10))
        texto = font.render("Presiona SPACE / clic para empezar", True, (255,255,255))
        screen.blit(texto, texto.get_rect(center=(W//2, H - 50)))
        pygame.display.flip()

    # reiniciar estado y empezar bucle principal
    obstaculos = []
    tiempo_para_prox_obstaculo = INTERVALO_OBSTACULO
    running = True

    while running:
        dt = clock.tick(120) / 1000.0

        

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

        # --- USO DE LA CÁMARA: LECTURA Y CONTROL CON DEDO ÍNDICE ---
        ret, frame = cap.read()
        cam_preview = None
        control_por_dedo = False
        results = None
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if hands is not None:
                try:
                    results = hands.process(rgb_frame)
                except Exception:
                    results = None
            else:
                results = None

            # convertir a surface para preview
            try:
                cam_surf = pygame.image.frombuffer(
                    rgb_frame.tobytes(),
                    (frame.shape[1], frame.shape[0]),
                    'RGB'
                )
                cam_preview = pygame.transform.scale(cam_surf, (320, 240))
            except:
                cam_preview = None

            # --- CONTROL DEL JUGADOR CON EL DEDO ÍNDICE ---
            if results and results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                index_tip = hand.landmark[8]

                # Mapeo completo cámara → pantalla (ajustar rango si es necesario)
                y_pantalla = np.interp(index_tip.y, [0.15, 0.85], [0, H])

                # Suavizado fluido
                suavizado = 0.55
                jugador["y"] = jugador["y"] * (1 - suavizado) + y_pantalla * suavizado

                # Límites
                jugador["y"] = max(0, min(H - 40, jugador["y"]))

                # DESACTIVAR gravedad cuando controlas con el dedo
                jugador["vy"] = 0
                control_por_dedo = True


        # FÍSICA
        if not control_por_dedo:
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

        # Dibujar preview de la cámara
        if cam_preview is not None:
            screen.blit(cam_preview, (W - 320 - 10, 10))
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
try:
    cap.release()
    cv2.destroyAllWindows()
except:
    pass
