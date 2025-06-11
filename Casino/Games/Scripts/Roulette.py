import pygame
import random
import json
import math
from Casino.Bank.Scripts.Bank import ChipData
from Casino.Bank.Scripts.chip import Chips
import sys
import os
import subprocess

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # oder feste Größe
screen_size = screen.get_size()

with open("../../Bank/Data/coin.json", "r") as f:
    daten = json.load(f)

def get_chip_counts(daten):
    keys = ["chip5_chips", "chip10_chips", "chip50_chips", "chip100_chips", "chip500_chips", "chip1000_chips", "chip5000_chips"]
    return [daten.get(key, 0) for key in keys]

chip_counts = get_chip_counts(daten)

# Füge den Projektroot-Pfad hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# Pfad zum Update-Skript
UPDATE_SCRIPT_PATH = os.path.join(project_root, "Casino", "User", "Data", "InsertIntoDatabase.py")


# Funktion zum Updaten der User Daten
def start_update_script():
    """Startet das Update-Skript als separater Prozess."""
    try:
        # Prüfe, ob das Update-Skript existiert
        if not os.path.exists(UPDATE_SCRIPT_PATH):
            print(f"Fehler: Update-Skript nicht gefunden: {UPDATE_SCRIPT_PATH}")
            return

        # Starte das Update-Skript als separater Prozess
        subprocess.Popen([sys.executable, UPDATE_SCRIPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Update-Skript wurde im Hintergrund gestartet.")
    except Exception as e:
        print(f"Fehler beim Starten des Update-Skripts: {str(e)}")

# === Farben ===
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (255, 255, 255)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

# Global definieren und sofort laden:
chip_images = {
    5: pygame.image.load("../../Bank/Data/Chip5.png").convert_alpha(),
    10: pygame.image.load("../../Bank/Data/Chip10.png").convert_alpha(),
    50: pygame.image.load("../../Bank/Data/Chip50.png").convert_alpha(),
    100: pygame.image.load("../../Bank/Data/Chip100.png").convert_alpha(),
    500: pygame.image.load("../../Bank/Data/Chip500.png").convert_alpha(),
    1000: pygame.image.load("../../Bank/Data/Chip1000.png").convert_alpha(),
    5000: pygame.image.load("../../Bank/Data/Chip5000.png").convert_alpha(),
}


WIDTH, HEIGHT = screen.get_size()
CENTER = (WIDTH // 4, HEIGHT // 2)
X_SCALE = WIDTH / 1920
Y_SCALE = HEIGHT / 1080
RADIUS = int(300 * X_SCALE)
SLICE_ANGLE = 360 / 37
clock = pygame.time.Clock()
circle_pos = [WIDTH // 2, HEIGHT // 2]
pygame.display.set_caption("Roulette")

try:
    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    coins = daten["coin"]

except FileNotFoundError:
    coins = 100
    daten = {"coin": coins}

numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30,
    8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7,
    28, 12, 35, 3, 26, 0
]

def draw_wheel():
    pygame.draw.circle(screen, BROWN, CENTER, int(360 * X_SCALE))
    pygame.draw.circle(screen, GOLD, CENTER, int(310 * X_SCALE))
    green_index = 37
    start_angle = -95 - SLICE_ANGLE * green_index
    angle = start_angle
    for i in range(38):
        color = GREEN if i == 37 else RED if i % 2 else BLACK
        draw_slice(angle, color, i)
        angle += SLICE_ANGLE
    pygame.draw.circle(screen, GOLD, CENTER, int(255 * X_SCALE))
    pygame.draw.circle(screen, GREEN, CENTER, int(245 * X_SCALE))
    pygame.draw.circle(screen, GOLD, CENTER, int(205 * X_SCALE))
    pygame.draw.circle(screen, BROWN, CENTER, int(195 * X_SCALE))
    pygame.draw.circle(screen, GOLD, CENTER, int(50 * X_SCALE))
    angle = start_angle
    for i in range(38):
        draw_edge(angle)
        angle += SLICE_ANGLE
    angle = start_angle
    for i in range(4):
        draw_Middle(angle)
        angle += 90
    angle = start_angle
    for i in range(4):
        draw_Points(angle)
        angle += 90

def draw_slice(angle, color, index):
    end_angle = angle + SLICE_ANGLE
    points = [CENTER]
    steps = 30
    for i in range(steps + 1):
        a = math.radians(angle + (i / steps) * (end_angle - angle))
        x = CENTER[0] + RADIUS * math.cos(a)
        y = CENTER[1] + RADIUS * math.sin(a)
        points.append((x, y))
    pygame.draw.polygon(screen, color, points)
    a = math.radians(angle + SLICE_ANGLE / 2)
    x = CENTER[0] + (RADIUS - 25 * X_SCALE) * math.cos(a)
    y = CENTER[1] + (RADIUS - 25 * Y_SCALE) * math.sin(a)
    font = pygame.font.SysFont("arial", int(20 * Y_SCALE))
    text = font.render(str(numbers[index]), True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def draw_edge(angle):
    # Nutze denselben Mittelwinkel wie in draw_slice
    a = math.radians((angle + 5) + SLICE_ANGLE / 2)

    # Skaliere die Radien basierend auf X/Y_SCALE
    outer_radius = 300 * X_SCALE
    inner_radius = 198 * X_SCALE  # passt zum inneren Kreis von draw_wheel()

    x1 = CENTER[0] + outer_radius * math.cos(a)
    y1 = CENTER[1] + outer_radius * math.sin(a)
    x2 = CENTER[0] + inner_radius * math.cos(a)
    y2 = CENTER[1] + inner_radius * math.sin(a)

    # Liniendicke ebenfalls skaliert
    line_width = max(1, int(6 * ((X_SCALE + Y_SCALE) / 2)))
    pygame.draw.line(screen, GOLD, (x1, y1), (x2, y2), line_width)

def draw_Middle(angle):
    a = math.radians(angle + SLICE_ANGLE / 2)
    avg_scale = (X_SCALE + Y_SCALE) / 2
    inner_circle_radius = 150 * X_SCALE
    x2 = CENTER[0] + inner_circle_radius * math.cos(a)
    y2 = CENTER[1] + inner_circle_radius * math.sin(a)
    line_width = max(1, int(10 * avg_scale))
    pygame.draw.line(screen, GOLD, CENTER, (x2, y2), line_width)


def draw_Points(angle):
    # Winkel auf die Mitte der Scheibe
    a = math.radians(angle + SLICE_ANGLE / 2)
    avg_scale = (X_SCALE + Y_SCALE) / 2
    # Den Punkt knapp außerhalb des innersten Gold-Rings platzieren
    point_radius_from_center = 160 * X_SCALE
    # Position berechnen
    x1 = CENTER[0] + point_radius_from_center * math.cos(a)
    y1 = CENTER[1] + point_radius_from_center * math.sin(a)
    # Punktradius responsive
    dot_radius = max(1, int(20 * avg_scale))
    pygame.draw.circle(screen, GOLD, (int(x1), int(y1)), dot_radius)

def scale(x, y):
    return int(x * X_SCALE), int(y * Y_SCALE)

def draw_field():

    def draw_line(start, end, width):
        pygame.draw.line(screen, WHITE, scale(*start), scale(*end), int(width * X_SCALE))

    draw_line((850, 100), (1900, 100), 10)
    draw_line((925, 200), (1900, 200), 10)
    draw_line((925, 300), (1900, 300), 10)
    draw_line((850, 400), (1900, 400), 10)
    draw_line((925, 500), (1825, 500), 10)
    draw_line((925, 600), (1825, 600), 10)
    draw_line((850, 100), (800, 250), 10)
    draw_line((850, 400), (800, 250), 10)

    for i in range(14):
        x = 925 + i * 75
        draw_line((x, 100), (x, 400), 10)

    for i in range(4):
        x = 925 + i * 300
        draw_line((x, 400), (x, 500), 10)

    for i in range(7):
        x = 925 + i * 150
        draw_line((x, 500), (x, 600), 10)

    font = pygame.font.SysFont(None, int(36 * Y_SCALE))
    labels = ["1st 12", "2nd 12", "3rd 12"]
    for i, x in enumerate([945, 1245, 1545]):
        sx, sy = scale(x, 420)
        pygame.draw.rect(screen, GOLD, (sx, sy, int(260 * X_SCALE), int(60 * Y_SCALE)))
        pygame.draw.rect(screen, GREEN, (sx + 2, sy + 2, int(256 * X_SCALE), int(56 * Y_SCALE)))
        text = font.render(labels[i], True, WHITE)
        text_rect = text.get_rect(center=(sx + int(130 * X_SCALE), sy + int(30 * Y_SCALE)))
        screen.blit(text, text_rect)

    labels = ["1 to 18", "EVEN", "ODD", "19 to 36"]
    for i, x in enumerate([945, 1095, 1545, 1695]):
        sx, sy = scale(x, 520)
        pygame.draw.rect(screen, GOLD, (sx, sy, int(110 * X_SCALE), int(60 * Y_SCALE)))
        pygame.draw.rect(screen, GREEN, (sx + 2, sy + 2, int(106 * X_SCALE), int(56 * Y_SCALE)))
        text = font.render(labels[i], True, WHITE)
        text_rect = text.get_rect(center=(sx + int(55 * X_SCALE), sy + int(30 * Y_SCALE)))
        screen.blit(text, text_rect)

    font_small = pygame.font.SysFont(None, int(18 * Y_SCALE))
    labels = ["2to1", "2to1", "2to1"]
    for i, y in enumerate([120, 220, 320]):
        sx, sy = scale(1845, y)
        pygame.draw.rect(screen, GOLD, (sx, sy, int(35 * X_SCALE), int(60 * Y_SCALE)))
        pygame.draw.rect(screen, GREEN, (sx + 2, sy + 2, int(31 * X_SCALE), int(56 * Y_SCALE)))
        text = font_small.render(labels[i], True, WHITE)
        text_rect = text.get_rect(center=(sx + int(17 * X_SCALE), sy + int(30 * Y_SCALE)))
        screen.blit(text, text_rect)

    def draw_diamond(x, y, size1, size2, color):
        x, y = scale(x, y)
        pygame.draw.polygon(screen, color, [
            (x, y - int(size1 * Y_SCALE)),
            (x + int(size2 * X_SCALE), y),
            (x, y + int(size1 * Y_SCALE)),
            (x - int(size2 * X_SCALE), y)
        ])

    diamonds = [
        (1300, 550, 40, 60, GOLD),
        (1300, 550, 38, 58, RED),
        (1450, 550, 40, 60, GOLD),
        (1450, 550, 38, 58, BLACK),
    ]

    for x, y, size1, size2, color in diamonds:
        draw_diamond(x, y, size1, size2, color)

    pygame.draw.ellipse(screen, GOLD, (*scale(838, 208), int(59 * X_SCALE), int(84 * Y_SCALE)))
    pygame.draw.ellipse(screen, GREEN, (*scale(840, 210), int(55 * X_SCALE), int(80 * Y_SCALE)))
    font = pygame.font.SysFont(None, int(36 * Y_SCALE))
    screen.blit(font.render("0", True, WHITE), scale(860, 240))

    def draw_color(color, x, y, number):
        x, y = scale(x, y)
        pygame.draw.ellipse(screen, color, (x, y, int(55 * X_SCALE), int(80 * Y_SCALE)))
        text = font.render(str(number), True, WHITE)
        text_rect = text.get_rect(center=(x + int(27 * X_SCALE), y + int(40 * Y_SCALE)))
        screen.blit(text, text_rect)

    rows = [
        [RED, BLACK, RED, BLACK, BLACK, RED, RED, BLACK, RED, BLACK, BLACK, RED],
        [BLACK, RED, BLACK, BLACK, RED, BLACK, BLACK, RED, BLACK, BLACK, RED, BLACK],
        [RED, BLACK, RED, RED, BLACK, RED, RED, BLACK, RED, RED, BLACK, RED]
    ]

    posx_start = 935
    posy_start = 310
    rows_count = len(rows)
    cols_count = len(rows[0])
    numbers = [[0 for _ in range(cols_count)] for _ in range(rows_count)]
    n = 1
    for col in range(cols_count):
        for row in range(rows_count):
            numbers[row][col] = n
            n += 1

    for row in range(rows_count):
        posy = posy_start - row * 100
        posx = posx_start
        for col in range(cols_count):
            draw_color(rows[row][col], posx, posy, numbers[row][col])
            posx += 75

    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    coins = daten["coin"]
    font = pygame.font.SysFont(None, int(36 * Y_SCALE))
    screen.blit(font.render(f"Coins: {coins}" , True, WHITE), scale(10, 10))


ball_visible = False
ball_position = None
last_result = None

def random_number():
    base_ball_radius = 225 * X_SCALE
    start_angle = -90
    SLICE_ANGLE = 360 / 37
    SLICE_ANGLE_HALF = (360 / 37)/2

    # Ziel-Sektor bestimmen
    target_index = random.randint(0, 36)
    target_angle = ((target_index * SLICE_ANGLE)-SLICE_ANGLE_HALF)
    target_angle = (target_angle - 90 + 95) % 360

    num_full_spins = random.randint(4, 5)
    total_spin_degrees = num_full_spins * 360 + target_angle
    angle = start_angle
    current_step = 20
    min_step = 1
    slowdown_factor = 0.99
    spinning = True

    while spinning:
        screen.fill((50, 50, 50))
        draw_wheel()
        draw_field()

        for chip in ChipData.get_all_chips():
            chip.draw(screen)

        rad = math.radians(angle % 360)
        ball_x = CENTER[0] + base_ball_radius * math.cos(rad)
        ball_y = CENTER[1] + base_ball_radius * math.sin(rad)

        ball_radius = int((HEIGHT / 900) * 12)
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

        pygame.display.flip()
        clock.tick(60)

        angle += current_step
        if current_step > min_step:
            current_step *= slowdown_factor

        if angle - start_angle >= total_spin_degrees:
            spinning = False

    def calculator():

        def is_red(n): return n in {
            1, 3, 5, 7, 9, 12, 14, 16, 18,
            19, 21, 23, 25, 27, 30, 32, 34, 36
        }
        def is_2(n): return n in {
            2, 5, 8, 11, 14, 17, 20, 23,
            26, 29, 32, 35
        }
        def is_1(n): return n in {
            1, 4, 7, 10, 13, 16, 19, 22,
            25, 28, 31, 34
        }

        posx_start = 935 + 30
        posy_start = 310 - 160

        # Field Hitboxes
        #numbers
        hitbox0 = pygame.Rect(*scale(860, 240), 20, 20)
        hitbox3 = pygame.Rect((posx_start + (75 * 0), posy_start + (100 * 0), 10, 10))
        hitbox6 = pygame.Rect((posx_start + (75 * 1), posy_start + (100 * 0), 10, 10))
        hitbox9 = pygame.Rect((posx_start + (75 * 2), posy_start + (100 * 0), 10, 10))
        hitbox12 = pygame.Rect((posx_start + (75 * 3), posy_start + (100 * 0), 10, 10))
        hitbox15 = pygame.Rect((posx_start + (75 * 4), posy_start + (100 * 0), 10, 10))
        hitbox18 = pygame.Rect((posx_start + (75 * 5), posy_start + (100 * 0), 10, 10))
        hitbox21 = pygame.Rect((posx_start + (75 * 6), posy_start + (100 * 0), 10, 10))
        hitbox24 = pygame.Rect((posx_start + (75 * 7), posy_start + (100 * 0), 10, 10))
        hitbox27 = pygame.Rect((posx_start + (75 * 8), posy_start + (100 * 0), 10, 10))
        hitbox30 = pygame.Rect((posx_start + (75 * 9), posy_start + (100 * 0), 10, 10))
        hitbox33 = pygame.Rect((posx_start + (75 * 10), posy_start + (100 * 0), 10, 10))
        hitbox36 = pygame.Rect((posx_start + (75 * 11), posy_start + (100 * 0), 10, 10))
        hitbox2 = pygame.Rect((posx_start + (75 * 0), posy_start + (100 * 1), 10, 10))
        hitbox5 = pygame.Rect((posx_start + (75 * 1), posy_start + (100 * 1), 10, 10))
        hitbox8 = pygame.Rect((posx_start + (75 * 2), posy_start + (100 * 1), 10, 10))
        hitbox11 = pygame.Rect((posx_start + (75 * 3), posy_start + (100 * 1), 10, 10))
        hitbox14 = pygame.Rect((posx_start + (75 * 4), posy_start + (100 * 1), 10, 10))
        hitbox17 = pygame.Rect((posx_start + (75 * 5), posy_start + (100 * 1), 10, 10))
        hitbox20 = pygame.Rect((posx_start + (75 * 6), posy_start + (100 * 1), 10, 10))
        hitbox23 = pygame.Rect((posx_start + (75 * 7), posy_start + (100 * 1), 10, 10))
        hitbox26 = pygame.Rect((posx_start + (75 * 8), posy_start + (100 * 1), 10, 10))
        hitbox29 = pygame.Rect((posx_start + (75 * 9), posy_start + (100 * 1), 10, 10))
        hitbox32 = pygame.Rect((posx_start + (75 * 10), posy_start + (100 * 1), 10, 10))
        hitbox35 = pygame.Rect((posx_start + (75 * 11), posy_start + (100 * 1), 10, 10))
        hitbox1 = pygame.Rect((posx_start + (75 * 0), posy_start + (100 * 2), 10, 10))
        hitbox4 = pygame.Rect((posx_start + (75 * 1), posy_start + (100 * 2), 10, 10))
        hitbox7 = pygame.Rect((posx_start + (75 * 2), posy_start + (100 * 2), 10, 10))
        hitbox10 = pygame.Rect((posx_start + (75 * 3), posy_start + (100 * 2), 10, 10))
        hitbox13 = pygame.Rect((posx_start + (75 * 4), posy_start + (100 * 2), 10, 10))
        hitbox16 = pygame.Rect((posx_start + (75 * 5), posy_start + (100 * 2), 10, 10))
        hitbox19 = pygame.Rect((posx_start + (75 * 6), posy_start + (100 * 2), 10, 10))
        hitbox22 = pygame.Rect((posx_start + (75 * 7), posy_start + (100 * 2), 10, 10))
        hitbox25 = pygame.Rect((posx_start + (75 * 8), posy_start + (100 * 2), 10, 10))
        hitbox28 = pygame.Rect((posx_start + (75 * 9), posy_start + (100 * 2), 10, 10))
        hitbox31 = pygame.Rect((posx_start + (75 * 10), posy_start + (100 * 2), 10, 10))
        hitbox34 = pygame.Rect((posx_start + (75 * 11), posy_start + (100 * 2), 10, 10))
        #colors
        hitboxred = pygame.Rect(1300, 550, 10, 10)
        hitboxblack = pygame.Rect(1450, 550, 10, 10)
        #even vs odd
        hitboxeven = pygame.Rect(1095, 520, int(110 * X_SCALE), int(60 * Y_SCALE))
        hitboxodd = pygame.Rect(1545, 520, int(110 * X_SCALE), int(60 * Y_SCALE))
        #1 to 18 vs 19 to 36
        hitbox1to18 = pygame.Rect(945, 520, int(110 * X_SCALE), int(60 * Y_SCALE))
        hitbox19to36 = pygame.Rect(1695, 520, int(110 * X_SCALE), int(60 * Y_SCALE))
        #1st 12 vs 2nd 12 vs 3rd 12
        hitbox1st12 = pygame.Rect(945, 420, int(260 * X_SCALE), int(60 * Y_SCALE))
        hitbox2nd12 = pygame.Rect(1245, 420, int(260 * X_SCALE), int(60 * Y_SCALE))
        hitbox3rd12 = pygame.Rect(1545, 420, int(260 * X_SCALE), int(60 * Y_SCALE))
        #rows
        hitbox2to1_1 = pygame.Rect(1845, 320, int(35 * X_SCALE), int(60 * Y_SCALE))
        hitbox2to1_2 = pygame.Rect(1845, 220, int(35 * X_SCALE), int(60 * Y_SCALE))
        hitbox2to1_3 = pygame.Rect(1845, 120, int(35 * X_SCALE), int(60 * Y_SCALE))

        number_hitboxes = [
            hitbox0, hitbox1, hitbox2, hitbox3, hitbox4, hitbox5,
            hitbox6, hitbox7, hitbox8, hitbox9, hitbox10, hitbox11,
            hitbox12, hitbox13, hitbox14, hitbox15, hitbox16, hitbox17,
            hitbox18, hitbox19, hitbox20, hitbox21, hitbox22, hitbox23,
            hitbox24, hitbox25, hitbox26, hitbox27, hitbox28, hitbox29,
            hitbox30, hitbox31, hitbox32, hitbox33, hitbox34, hitbox35, hitbox36
        ]

        all_chips = ChipData.get_all_chips()
        config = ChipData.chip_configs()



        gewinn = 0
        verlust = 0

        for chip in all_chips:
            # Zahlenfelder
            for i, hitbox in enumerate(number_hitboxes):
                if chip.collides_with_rect(hitbox):
                    numbers = i
                    for conf in config:
                        if f"chip{conf['value']}_" in chip.name.lower():
                            if numbers == result and 0 <= result <= 36:
                                gewinn += conf["value"] * 35
                            else:
                                verlust += conf["value"]
                    break  # Kein weiteres Feld prüfen

            # Farben
            if chip.collides_with_rect(hitboxred):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if is_red(result):
                            gewinn += conf["value"]
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitboxblack):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if is_red != result and result != 0:
                            gewinn += conf["value"]
                        else:
                            verlust += conf["value"]

            # Gerade/Ungerade
            if chip.collides_with_rect(hitboxeven):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if result % 2 == 0 and result != 0:
                            gewinn += conf["value"]
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitboxodd):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if result != 0 and result % 2 != 0:
                            gewinn += conf["value"]
                        else:
                            verlust += conf["value"]

            # 1–18 vs 19–36
            if chip.collides_with_rect(hitbox1to18):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if 1 <= result <= 18:
                            gewinn += conf["value"]
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitbox19to36):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if 19 <= result <= 36:
                            gewinn += conf["value"]
                        else:
                            verlust += conf["value"]

            # Dutzende
            if chip.collides_with_rect(hitbox1st12):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if 1 <= result <= 12:
                            gewinn += conf["value"] * 2
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitbox2nd12):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if 13 <= result <= 24:
                            gewinn += conf["value"] * 2
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitbox3rd12):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if 25 <= result <= 36:
                            gewinn += conf["value"] * 2
                        else:
                            verlust += conf["value"]

            # Reihen
            if chip.collides_with_rect(hitbox2to1_1):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if result % 3 == 0:
                            gewinn += conf["value"] * 2
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitbox2to1_2):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if is_2(result):
                            gewinn += conf["value"] * 2
                        else:
                            verlust += conf["value"]
            elif chip.collides_with_rect(hitbox2to1_3):
                for conf in config:
                    if f"chip{conf['value']}_" in chip.name.lower():
                        if is_1(result):
                            gewinn += conf["value"] * 2
                        else:
                            verlust += conf["value"]

        gewinn -= verlust

        daten["coin"] += gewinn
        with open("../../Bank/Data/coin.json", "w") as f:
            json.dump(daten, f, indent=4)

    # Ergebnis berechnen
    global ball_position, ball_visible, last_result

    # Finale Zahl berechnen
    final_angle = angle % 360
    adjusted_angle = (final_angle + 95) % 360  # Korrektur je nach Startwinkel / Ausrichtung
    index = int(adjusted_angle // SLICE_ANGLE)
    result = numbers[index]

    ball_position = (int(ball_x), int(ball_y))  # speichere Ballposition
    last_result = result
    ball_visible = True  # Ball soll nun angezeigt bleiben
    print(result)
    calculator()

def chips_back_to_spawn():

    configs = ChipData.chip_configs()
    ypos_start = HEIGHT * 0.85
    xpos = WIDTH * 0.55

    for config in configs:
        chip_list = config["list"]
        for index, chip in enumerate(chip_list):
            ypos = ypos_start - index   # stapeln nach oben
            chip.pos = (xpos, ypos)        # neue Position setzen
        xpos += WIDTH * 0.06  # nächster Stapel nach rechts



def spawn_all_chips():
    global chip_images  # auf globale Variable zugreifen
    ypos = HEIGHT * 0.85
    xpos = WIDTH * 0.5
    orxpos = WIDTH * 0.5

    configs = ChipData.chip_configs()

    for config in configs:
        config["list"].clear()

    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    chip_counts = get_chip_counts(daten)

    for index, config in enumerate(configs):
        value = config["value"]
        count = chip_counts[index]
        chip_list = config["list"]
        image = chip_images[value]

        if value not in chip_images:
            chip_images[value] = pygame.image.load(f"../../Bank/Data/Chip{value}.png").convert_alpha()

        image = chip_images[value]
        namenumber = 1

        for i in range(count):
            chip = Chips(image, (xpos, ypos), screen_size)
            chip.name = f"chip{value}_{namenumber}"
            chip_list.append(chip)
            namenumber += 1
            ypos -= 1
        ypos = HEIGHT * 0.85
        xpos += 0.06

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Roulette")
    active_chip = None
    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)

    if daten["is_spawned"] == 0:
        spawn_all_chips()
        daten["is_spawned"] = 1
        with open("../../Bank/Data/coin.json", "w") as f:
            json.dump(daten, f, indent=4)
    all_chips = ChipData.get_all_chips()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Nur bei Tastendruck hat event.key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # chip_counts speichern
                    chip_counts = [0] * len(ChipData.chip_configs())
                    for index, config in enumerate(ChipData.chip_configs()):
                        chip_counts[index] = len(config["list"])

                    with open("../../Bank/Data/coin.json", "r") as f:
                        daten = json.load(f)
                    daten["is_spawned"] = 0  # neue Chips beim Start

                    with open("../../Bank/Data/coin.json", "w") as f:
                        json.dump(daten, f, indent=4)
                    start_update_script()
                    return


                elif event.key == pygame.K_SPACE:
                    # Neue Kugel drehen
                    random_number()

                elif event.key == pygame.K_g:
                    all_chips = ChipData.get_all_chips()
                    chips_back_to_spawn()

            # === Chip Drag & Drop ===
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for chip in reversed(all_chips):  # nur obersten Chip aktivieren
                    if chip.collides_with_point(event.pos):
                        active_chip = chip
                        chip.dragging = True
                        mouse_x, mouse_y = event.pos
                        chip.drag_offset = (
                            mouse_x - chip.pos[0],
                            mouse_y - chip.pos[1]
                        )
                        # Chip nach oben bringen
                        all_chips.remove(chip)
                        all_chips.append(chip)
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if active_chip:
                    active_chip.dragging = False
                    active_chip = None

            elif event.type == pygame.MOUSEMOTION:
                if active_chip and active_chip.dragging:
                    mouse_x, mouse_y = event.pos
                    active_chip.pos = (
                        mouse_x - active_chip.drag_offset[0],
                        mouse_y - active_chip.drag_offset[1]
                    )

        # Frame zeichnen
        screen.fill((50, 50, 50))
        draw_wheel()
        draw_field()
        for chip in all_chips:
            chip.draw(screen)

        ball_radius = int((HEIGHT / 900) * 12)
        if ball_visible and ball_position:
            pygame.draw.circle(screen, WHITE, ball_position, ball_radius)

        pygame.display.flip()
        clock.tick(60)

    # Nach Verlassen der Schleife: Pygame beenden
    print("Thanks for playing!")
    pygame.quit()

if __name__ == "__main__":
    main()