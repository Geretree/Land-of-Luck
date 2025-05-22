from itertools import count

import pygame
import random
import json
import math
import sys


# === Farben ===
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (255, 255, 255)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
CENTER = (WIDTH // 4, HEIGHT // 2)
X_SCALE = WIDTH / 1920
Y_SCALE = HEIGHT / 1080
RADIUS = int(300 * X_SCALE)
SLICE_ANGLE = 360 / 37
clock = pygame.time.Clock()
circle_pos = [WIDTH // 2, HEIGHT // 2]
pygame.display.set_caption("Roulette")


# Lade Coins
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
        draw_Edge(angle)
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


def draw_Edge(angle):
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

#---------------------------------SPIELFUNKTION-------------------------------
ball_visible = False
ball_position = None
last_result = None

def random_number():
    base_ball_radius = 187
    scaled_ball_radius = int((HEIGHT / 900) * base_ball_radius)
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

        rad = math.radians(angle % 360)
        ball_x = CENTER[0] + scaled_ball_radius * math.cos(rad)
        ball_y = CENTER[1] + scaled_ball_radius * math.sin(rad)

        ball_radius = int((HEIGHT / 900) * 12)
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

        pygame.display.flip()
        clock.tick(60)

        angle += current_step
        if current_step > min_step:
            current_step *= slowdown_factor

        if angle - start_angle >= total_spin_degrees:
            spinning = False

    global ball_position, ball_visible, last_result
    ball_position = (int(ball_x), int(ball_y))
    last_result = numbers[target_index]
    result = last_result
    ball_visible = True


    def calculator():

        def is_red(n): return n in {
            1, 3, 5, 7, 9, 12, 14, 16, 18,
            19, 21, 23, 25, 27, 30, 32, 34, 36
        }
        def is_2(n): return n in {
            2, 5, 8, 11, 14, 17, 20, 23,
            26, 29, 32, 35
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

        x1 = 850
        y1 = 100
        x2 = 1900
        y2 = 600

        # Calculate top-left and size
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        hitbox_for_field = pygame.Rect(left, top, width, height)


        num0 = 100
        numbers = 0
        red = 0
        black = 0
        even = 0
        odd = 0
        one_to_eighteen = 0
        nineteen_to_thirtysix = 0
        one_to_twelve = 0
        thirteen_to_twentyfour = 0
        twentyfive_to_thirtysix = 0
        st_row = 0
        nd_row = 0
        rd_row = 0

        number_hitboxes = [
            hitbox0, hitbox1, hitbox2, hitbox3, hitbox4, hitbox5,
            hitbox6, hitbox7, hitbox8, hitbox9, hitbox10, hitbox11,
            hitbox12, hitbox13, hitbox14, hitbox15, hitbox16, hitbox17,
            hitbox18, hitbox19, hitbox20, hitbox21, hitbox22, hitbox23,
            hitbox24, hitbox25, hitbox26, hitbox27, hitbox28, hitbox29,
            hitbox30, hitbox31, hitbox32, hitbox33, hitbox34, hitbox35, hitbox36
        ]
        count = 0

        for chip in get_all_chips():
            # Zahlenfelder
            for i, hitbox in enumerate(number_hitboxes):
                if chip.collides_with_rect(hitbox):
                    print(f"{chip.name} liegt auf Zahl {i}")
                    numbers = i
                    break  # Kein weiteres Feld prüfen

            # Farben
            if chip.collides_with_rect(hitboxred):
                red = 1
            elif chip.collides_with_rect(hitboxblack):
                black = 1

            # Gerade/Ungerade
            if chip.collides_with_rect(hitboxeven):
                even = 1
            elif chip.collides_with_rect(hitboxodd):
                odd = 1

            # 1–18 vs 19–36
            if chip.collides_with_rect(hitbox1to18):
                one_to_eighteen = 1
            elif chip.collides_with_rect(hitbox19to36):
                nineteen_to_thirtysix = 1

            # Dutzende
            if chip.collides_with_rect(hitbox1st12):
                one_to_twelve = 1
            elif chip.collides_with_rect(hitbox2nd12):
                thirteen_to_twentyfour = 1
            elif chip.collides_with_rect(hitbox3rd12):
                twentyfive_to_thirtysix = 1

            # Reihen
            if chip.collides_with_rect(hitbox2to1_1):
                st_row = 1
            elif chip.collides_with_rect(hitbox2to1_2):
                nd_row = 1
            elif chip.collides_with_rect(hitbox2to1_3):
                rd_row = 1


            if chip.collides_with_rect(hitbox_for_field):
                count += 1
                print("hello")
                print(count)

        gewinn = 0
        verlusst = 0

        if num0 == 0 and result == 0:
            print("You bet on 0 and won!")
            gewinn += 5 * 36

        if numbers == result and 1 <= result <= 36:
            print(f"You bet on {result} and won!")
            gewinn += 5 * 36

        if red == 1 and is_red(result):
            print("You bet on Red and won!")
            gewinn += 5 * 2
        elif black == 1 and result != 0:
            print("You bet on Black and won!")
            gewinn += 5 * 2

        if even == 1 and result % 2 == 0 and result != 0:
            print("You bet on Even and won!")
            gewinn += 5 * 2
        elif odd == 1 and result % 2 != 0:
            print("You bet on Odd and won!")
            gewinn += 5 * 2

        if one_to_eighteen == 1 and 1 <= result <= 18:
            print("You bet on 1 to 18 and won!")
            gewinn += 5 * 2
        elif nineteen_to_thirtysix == 1 and 19 <= result <= 36:
            print("You bet on 19 to 36 and won!")
            gewinn += 5 * 2

        if one_to_twelve == 1 and 1 <= result <= 12:
            print("You bet on 1 to 12 and won!")
            gewinn += 5 * 3
        elif thirteen_to_twentyfour == 1 and 13 <= result <= 24:
            print("You bet on 13 to 24 and won!")
            gewinn += 5 * 3
        elif twentyfive_to_thirtysix == 1 and 25 <= result <= 36:
            print("You bet on 25 to 36 and won!")
            gewinn += 5 * 3

        if rd_row == 1 and result % 3 == 0:
            print("You bet on the third row and won!")
            gewinn += 5 * 3
        elif nd_row == 1 and is_2(result):
            print("You bet on the second row and won!")
            gewinn += 5 * 3
        elif st_row == 1 and result != 0:
            print("You bet on the first row and won!")
            gewinn += 5 * 3

        gewinn -= 5

        daten["coin"] += gewinn
        with open("../../Bank/Data/coin.json", "w") as f:
            json.dump(daten, f, indent=4)
    print(result)
    calculator()


from Casino.Bank.Scripts.chip import Chips
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # oder feste Größe
screen_size = screen.get_size()
chip5_chips = []
chip10_chips = []
chip50_chips = []
chip100_chips = []
chip500_chips = []
chip1000_chips = []
chip5000_chips = []


def get_all_chips():
    return chip5_chips + chip10_chips + chip50_chips + chip100_chips + chip500_chips + chip1000_chips + chip5000_chips

def spawn_all_chips():
    xpos = 1000
    ypos = 900

    chip_configs = [
        {"value": 5, "count": 30, "list": chip5_chips},
        {"value": 10, "count": 70, "list": chip10_chips},
        {"value": 50, "count": 10, "list": chip50_chips},
        {"value": 100, "count": 40, "list": chip100_chips},
        {"value": 500, "count": 200, "list": chip500_chips},
        {"value": 1000, "count": 5, "list": chip1000_chips},
        {"value": 5000, "count": 2, "list": chip5000_chips}
    ]


    for config in chip_configs:
        value = config["value"]
        count = config["count"]
        chip_list = config["list"]
        namenumber = 1
        for i in range(count):
            chip = Chips(f"../../Bank/Data/Chip{value}.png", (xpos, ypos), screen_size)
            chip.name = f"chip{value}_{namenumber}"
            chip_list.append(chip)
            namenumber = (namenumber + 1)
            print(chip.name)
            ypos -= 1
        ypos = 900
        xpos += 100


# Wenn du die Fenstergröße änderst:
new_size = screen.get_size()

import asyncio

# === Spielschleife ===
spawn_all_chips()
running = True
active_chip = None
dragged_chips = []


while running and coins > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Nur bei Tastendruck hat event.key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

                # Wechsle ins Lobby-Modul (async-Funktion korrekt starten)
                from Casino.Lobby.Scripts.Lobby import game

                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    asyncio.run(game())
                else:
                    loop.create_task(game())

                break  # verlasse die for-Schleife; while endet durch running=False

            elif event.key == pygame.K_SPACE:
                # Neue Kugel drehen
                ball_visible = False
                ball_position = None
                last_result = None
                random_number()

        # === Chip Drag & Drop ===
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for chip in reversed(get_all_chips()):  # nur obersten Chip aktivieren
                if chip.collides_with_point(event.pos):
                    active_chip = chip
                    chip.dragging = True
                    mouse_x, mouse_y = event.pos
                    chip.drag_offset = (
                        mouse_x - chip.pos[0],
                        mouse_y - chip.pos[1]
                    )
                    # Chip nach oben bringen
                    get_all_chips().remove(chip)
                    get_all_chips().append(chip)
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
    for chip in get_all_chips():
        chip.draw(screen)

    if ball_visible and ball_position:
        pygame.draw.circle(screen, WHITE, ball_position, 12)

    pygame.display.flip()
    clock.tick(60)

# Nach Verlassen der Schleife: Pygame beenden
print("Thanks for playing!")
pygame.quit()
sys.exit()
