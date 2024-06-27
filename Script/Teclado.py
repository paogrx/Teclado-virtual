import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Deshabilitar mensajes de advertencia

import mediapipe as mp
import cv2
from pynput.keyboard import Controller

# Inicialización de las utilidades de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicialización de la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Inicialización del controlador del teclado
keyboard = Controller()

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Obtener el tamaño de la ventana
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Definir el teclado en pantalla
teclas = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
    ['Ctrl', 'Space', 'Borrar', 'Limpiar']  # Eliminada la tecla 'Alt'
]

# Ajustar el tamaño y el espaciado de las teclas
num_teclas_max = max(len(fila) for fila in teclas)  # Número máximo de teclas en una fila
tecla_ancho = (width - 40) // num_teclas_max  # Ajustar el ancho de las teclas
tecla_alto = height // (len(teclas) + 2)
espacio_horizontal = 5
espacio_vertical = 5

# Estado de las teclas de modificador
shift_presionado = False
ctrl_presionado = False

# Texto escrito
texto_escrito = ""

# Historial de posiciones del índice
historial_posiciones = []

# Función para dibujar el teclado en la imagen
def dibujar_teclado(image):
    start_x = 10  # Posición inicial horizontal del teclado
    start_y = height - (tecla_alto + espacio_vertical) * len(teclas) - 20  # Posición inicial vertical del teclado
    for fila in teclas:
        x = start_x
        for tecla in fila:
            ancho_actual = tecla_ancho
            if tecla in ['Space', 'Borrar', 'Limpiar']:
                if tecla == 'Space':
                    ancho_actual = tecla_ancho * 4 + 3 * espacio_horizontal  # Hacer la barra espaciadora más larga
                elif tecla == 'Borrar' or tecla == 'Limpiar':
                    ancho_actual = tecla_ancho * 2 + 2 * espacio_horizontal  # Ajustar el ancho de las teclas Borrar y Limpiar
            cv2.rectangle(image, (x, start_y), (x + ancho_actual, start_y + tecla_alto), (255, 255, 255), 2)
            cv2.putText(image, tecla, (x + 5, start_y + tecla_alto - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            x += ancho_actual + espacio_horizontal
        start_y += tecla_alto + espacio_vertical

# Función para dibujar el texto escrito en la imagen
def dibujar_texto(image):
    global texto_escrito
    # Definir la posición y el tamaño del texto
    cv2.putText(image, texto_escrito, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

# Función para calcular la distancia entre dos puntos
def calcular_distancia(punto1, punto2):
    return ((punto1[0] - punto2[0]) ** 2 + (punto1[1] - punto2[1]) ** 2) ** 0.5

# Función para detectar si un dedo toca una tecla
def detectar_tecla(x, y):
    start_x = 10
    start_y = height - (tecla_alto + espacio_vertical) * len(teclas) - 20
    for fila in teclas:
        current_x = start_x
        for tecla in fila:
            ancho_actual = tecla_ancho
            if tecla in ['Space', 'Borrar', 'Limpiar']:
                if tecla == 'Space':
                    ancho_actual = tecla_ancho * 4 + 3 * espacio_horizontal  # Hacer la barra espaciadora más larga
                elif tecla == 'Borrar' or tecla == 'Limpiar':
                    ancho_actual = tecla_ancho * 2 + 2 * espacio_horizontal  # Ajustar el ancho de las teclas Borrar y Limpiar
            if current_x <= x <= current_x + ancho_actual and start_y <= y <= start_y + tecla_alto:
                return tecla
            current_x += ancho_actual + espacio_horizontal
        start_y += tecla_alto + espacio_vertical
    return None

# Función para manejar la entrada de la tecla detectada
def manejar_tecla(tecla):
    global shift_presionado, ctrl_presionado, texto_escrito

    if tecla == 'Shift':
        shift_presionado = not shift_presionado
        return
    elif tecla == 'Ctrl':
        ctrl_presionado = not ctrl_presionado
        return
    elif tecla == 'Space':
        tecla = ' '
    elif tecla == 'Enter':
        tecla = '\n'
    elif tecla == 'Borrar':
        if texto_escrito:
            texto_escrito = texto_escrito[:-1]
            # Simular el borrado de una tecla
            keyboard.press('\b')
            keyboard.release('\b')
        return
    elif tecla == 'Limpiar':
        texto_escrito = ""
        return

    if shift_presionado:
        if len(tecla) == 1:  # Si es una letra, convertir a mayúscula
            tecla = tecla.upper()
        else:
            # Mapeo de caracteres especiales con Shift (puedes expandir esta lista según sea necesario)
            shift_map = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
                         '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '\"', ',': '<', '.': '>', '/': '?'}
            tecla = shift_map.get(tecla, tecla)
        shift_presionado = False

    texto_escrito += tecla
    print(f"Tecla pulsada: {tecla}")
    keyboard.press(tecla)
    keyboard.release(tecla)

# Función para detectar un gesto de pulsación
def detectar_gesto(historial):
    if len(historial) < 2:
        return False
    # Detectar si el movimiento es hacia abajo
    movimiento_y = historial[-1][1] - historial[0][1]
    if movimiento_y > 30:  # Ajustar este valor según sea necesario
        return True
    return False

try:
    # Configuración de MediaPipe Hands
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignorando fotograma vacío de la cámara.")
                continue

            # Convertir la imagen de BGR a RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False  # Optimización para mejorar el rendimiento
            results = hands.process(image_rgb)
            
            # Convertir la imagen de vuelta a BGR para OpenCV
            image_rgb.flags.writeable = True
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Dibujar el texto escrito en la imagen
            dibujar_texto(image_bgr)

            # Dibujar el teclado en la imagen
            dibujar_teclado(image_bgr)

            # Dibujar las anotaciones de las manos en la imagen
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Obtener las coordenadas del índice
                    index_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_bgr.shape[1])
                    index_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_bgr.shape[0])
                    
                    # Guardar la posición en el historial
                    historial_posiciones.append((index_x, index_y))
                    
                    if len(historial_posiciones) > 5:  # Mantener un historial limitado
                        historial_posiciones.pop(0)
                    
                    # Dibujar un círculo en la punta del índice
                    cv2.circle(image_bgr, (index_x, index_y), 10, (0, 255, 0), -1)
                    
                    # Detectar si se ha realizado un gesto de pulsación
                    if detectar_gesto(historial_posiciones):
                        tecla_detectada = detectar_tecla(index_x, index_y)
                        if tecla_detectada:
                            manejar_tecla(tecla_detectada)
                            historial_posiciones.clear()  # Limpiar el historial para detectar la próxima pulsación

            # Mostrar la imagen con las anotaciones
            cv2.imshow('Teclado Virtual', image_bgr)

            if cv2.waitKey(1) & 0xFF == 27:  # Presionar 'Esc' para salir
                break
except KeyboardInterrupt:
    pass
finally:
    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()

