import pygame
import math
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras import layers

class PozycjaMenu:
    def __init__(self, nazwa, status=True):
        self.nazwa = nazwa
        self.status = status
    
    def zmien_status(self):
        self.status = not self.status

# Parametry okna
WIDTH, HEIGHT = 1080, 720

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Parametry robota
SENSOR_RANGE = 10
SPEED = 1.5
ROBOT_RADIUS = 15
TURN_RATE = 3

# Próg dla zmiany koloru sensora
SENSOR_THRESHOLD = SENSOR_RANGE / 2

def screen_width():
    return WIDTH

def screen_height():
    return HEIGHT

# Inicjalizacja Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulator Robota")


# Funkcja rysująca ramkę wokół okna gry
def draw_frame():
    pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, 10))  # Górna krawędź
    pygame.draw.rect(WIN, BLACK, (0, 0, 10, HEIGHT))  # Lewa krawędź
    pygame.draw.rect(WIN, BLACK, (WIDTH - 10, 0, 10, HEIGHT))  # Prawa krawędź
    pygame.draw.rect(WIN, BLACK, (0, HEIGHT - 10, WIDTH, 10))  # Dolna krawędź


# Funkcja rysująca spiralę
def draw_spiral():
    global end_pos
    x, y = WIDTH // 2, HEIGHT // 2
    end_pos = x, y
    length = 8
    angle = 0

    while length < min(WIDTH, HEIGHT):
        new_x = x + length * math.cos(math.radians(angle))
        new_y = y + length * math.sin(math.radians(angle))
        pygame.draw.line(WIN, BLACK, (x, y), (new_x, new_y), 10)
        x, y = new_x, new_y
        angle += 45
        length += 8

def hex_to_rgb(hex_color):
  
    # Usuń znak '#' z początku wartości HEX
    hex_color = hex_color.lstrip('#')

    # Sprawdź długość wartości HEX
    if len(hex_color) != 6:
        raise ValueError(f"Nieprawidłowa wartość HEX: {hex_color}")

    # Podziel wartość HEX na składowe
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]

    # Konwertuj wartości HEX na wartości dziesiętne
    r = int(r, 16)
    g = int(g, 16)
    b = int(b, 16)

    # Zwróć wartości RGB jako krotkę
    return (r, g, b)

# Funkcja rysująca robota
def draw_robot(x, y, angle):
    pygame.draw.circle(WIN, RED, (int(x), int(y)), ROBOT_RADIUS)
    sensor_x = x + ROBOT_RADIUS * math.cos(math.radians(angle))
    sensor_y = y - ROBOT_RADIUS * math.sin(math.radians(angle))
    pygame.draw.line(WIN, GREEN, (x, y), (sensor_x, sensor_y), 2)


# Funkcja sprawdzająca odległość do przeszkód za pomocą sensora
def check_sensor(x, y, angle, offset_angle=0):
    sensor_angle = angle + offset_angle
    sensor_x = x + ROBOT_RADIUS * math.cos(math.radians(sensor_angle))
    sensor_y = y - ROBOT_RADIUS * math.sin(math.radians(sensor_angle))
    for i in range(SENSOR_RANGE):
        check_x = int(sensor_x + i * math.cos(math.radians(sensor_angle)))
        check_y = int(sensor_y - i * math.sin(math.radians(sensor_angle)))
        if 0 <= check_x < WIDTH and 0 <= check_y < HEIGHT:
            if WIN.get_at((check_x, check_y)) == BLACK:
                return i
    return SENSOR_RANGE


# Funkcja przekształcająca stan do formatu wykorzystywanego przez DQN
def get_state(x, y, angle):
    front_sensor = check_sensor(x, y, angle)
    left_sensor = check_sensor(x, y, angle, -45)
    right_sensor = check_sensor(x, y, angle, 45)
    return np.array([front_sensor, left_sensor, right_sensor], dtype=np.float32) / SENSOR_RANGE

# Funkcja ruchu robota
def move_robot(x, y, angle):

    front_sensor_distance = check_sensor(x, y, angle)
    left_sensor_distance = check_sensor(x, y, angle, 45)
    right_sensor_distance = check_sensor(x, y, angle, -45)

    if front_sensor_distance < SENSOR_THRESHOLD or left_sensor_distance < SENSOR_THRESHOLD or right_sensor_distance < SENSOR_THRESHOLD:
        angle += TURN_RATE
    else:
        x += SPEED * math.cos(math.radians(angle))
        y -= SPEED * math.sin(math.radians(angle))

    return x, y, angle, front_sensor_distance, left_sensor_distance, right_sensor_distance

# Funkcja rysująca odczyty sensorów
def draw_sensors(front_sensor, left_sensor, right_sensor):
    sensor_width = 30
    max_height = 100
    
    # Przeskalowanie wartości sensorów
    front_height = int((1 - front_sensor / SENSOR_RANGE) * max_height)
    left_height = int((1 - left_sensor / SENSOR_RANGE) * max_height)
    right_height = int((1 - right_sensor / SENSOR_RANGE) * max_height)
    
    # Ustawienie koloru na czerwony, jeśli odległość przekracza próg
    front_color = RED if front_sensor < SENSOR_THRESHOLD else GREEN
    left_color = RED if left_sensor < SENSOR_THRESHOLD else GREEN
    right_color = RED if right_sensor < SENSOR_THRESHOLD else GREEN

    # Rysowanie słupków w prawym dolnym rogu sceny
    pygame.draw.rect(WIN, left_color, (WIDTH - 90 - 10, HEIGHT - left_height - 10, sensor_width, left_height))
    pygame.draw.rect(WIN, front_color, (WIDTH - 60 - 10, HEIGHT - front_height - 10, sensor_width, front_height))
    pygame.draw.rect(WIN, right_color, (WIDTH - 30 - 10, HEIGHT - right_height - 10, sensor_width, right_height))


def main():

    menu = [
        PozycjaMenu("Pozycja robota", False),
        PozycjaMenu("Wygenerowanie ścieżki", False),
        PozycjaMenu("Trenowanie modelu", False),
        PozycjaMenu("Użycie nauczonego modelu", False),
        PozycjaMenu("Start/Stop robot - Pause", False),
        PozycjaMenu("Zapisanych danych do trenowania modelu", False),
        PozycjaMenu("Robot u celu", False)
    ]

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    #paused = False  # Flaga oznaczająca, czy symulacja jest zatrzymana
    run = True
    ready = False

    angle = random.randint(0, 360)  # Losowy kąt początkowy
    front_sensor = left_sensor = right_sensor = 1000
    # Zmienne do zapisywania ścieżki
    path_data = []
    dist = screen_width()

    while run:
        clock.tick(30)
        WIN.fill((116,161,142))

        draw_frame()  # Rysowanie ramki wokół okna gry
        draw_spiral()  

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if ready:
                        #paused = not paused  # Zmiana stanu pauzy po wciśnięciu klawisza SPACJA
                        pozycja_menu = menu[4]
                        pozycja_menu.zmien_status()
                        print(f"{pozycja_menu.nazwa}")                       
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not menu[0].status: # nie można wybrać nowej pozycji robota po rozpoczęciu procesu generowania danych
                    x, y = event.pos
                    ready = True
                    # Zmiana statusu wybranej pozycji menu
                    pozycja_menu = menu[0]
                    pozycja_menu.zmien_status()
                    print(f"{pozycja_menu.nazwa}")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and ready:
                    if not menu[1].status: 
                        # Zmiana statusu wybranej pozycji menu
                        pozycja_menu = menu[1]
                        pozycja_menu.zmien_status()
                        print(f"{pozycja_menu.nazwa}")

        # go if not paused and press 1:
        if menu[1].status and not menu[4].status: 
            dist = math.sqrt((x - end_pos[0]) ** 2 + (y - end_pos[1]) ** 2)
            state = get_state(x, y, angle)
            next_x, next_y, next_angle, front_sensor, left_sensor, right_sensor = move_robot(x, y, angle)
            next_state = get_state(next_x, next_y, next_angle)
            reward = 1  # Nagroda 
            done = (dist < 20)
            path_data.append((next_state, 1, reward, next_state, done))  # action = 1 to ruch do przodu
            x, y, angle = next_x, next_y, next_angle
            pass      

        if dist < 20 and not menu[6].status:
            text1 = font.render(f'Robot u celu!', True, hex_to_rgb("#F9EBC7"))
            WIN.blit(text1, (screen_width() - text1.get_rect().width - 15, 15))
            text1 = font.render(f'Dane gotowe do zapisania!', True, hex_to_rgb("#F9EBC7"))
            WIN.blit(text1, (screen_width() - text1.get_rect().width -15, 45))

            # przerywamy generowanie danych
            pozycja_menu = menu[]
            pozycja_menu.zmien_status()
            print(f"{pozycja_menu.nazwa}")

            pass

        draw_sensors(front_sensor, left_sensor, right_sensor)

        if ready:
            draw_robot(x, y, angle)

        # Target
        pygame.draw.circle(WIN, (0,255,204), (end_pos[0], end_pos[1]), ROBOT_RADIUS-4)

        esc_text = font.render(f'Exit, press esc', True, hex_to_rgb("#F6CD44"))
        WIN.blit(esc_text, (15, 15))
        
        if menu[0].status:
            text2 = font.render(f'[LMB] : krok 1: Pozycja robota określona', True, hex_to_rgb("#00ff00"))
            WIN.blit(text2, (15, 45))
        else:
            text2 = font.render(f'[LMB] : krok 1: Określ pozycję robota', True, hex_to_rgb("#ff0000"))
            WIN.blit(text2, (15, 45))

        if menu[1].status and not menu[4].status:
            text2 = font.render(f'[1] : krok 2: Przejazdu przez labirynt - generowanie danych uczacych', True, hex_to_rgb("#00ff00"))
            WIN.blit(text2, (15, 75))
        elif menu[1].status and menu[4].status: # pressed 1 and paused
            text2 = font.render(f'[1] : krok 2: Przejazdu przez labirynt - generowanie danych uczacych [Paused!]', True, hex_to_rgb("#ff0000"))
            WIN.blit(text2, (15, 75))
        else:
            text2 = font.render(f'[1] : krok 2: Przejazdu przez labirynt - generowanie danych uczacych', True, hex_to_rgb("#ff0000"))
            WIN.blit(text2, (15, 75))

        if menu[5].status:
            text2 = font.render(f'[2] : krok 3: Zapisywanie trasy', True, hex_to_rgb("#00ff00"))
            WIN.blit(text2, (15, 105))
        else:
            text2 = font.render(f'[2] : krok 3: Zapisywanie trasy', True, hex_to_rgb("#ff0000"))
            WIN.blit(text2, (15, 105))

        pygame.display.update()     

    pygame.quit()




if __name__ == "__main__":
    main()