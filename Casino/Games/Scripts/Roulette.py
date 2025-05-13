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

def draw_field():
    def scale(x, y):
        return int(x * X_SCALE), int(y * Y_SCALE)

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

#---------------------------------SPIELFUNKTION-------------------------------
ball_visible = False
ball_position = None
last_result = None




def random_number():
    rand_index = random.randint(0, 36)
    wheel_numbers = [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,
        13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1,
        20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0
    ]

    # Dynamischer Radius auf Basis der Bildschirmhöhe
    base_ball_radius = 187  # Ursprünglich bei Höhe 900
    scaled_ball_radius = int((HEIGHT / 900) * base_ball_radius)

    start_angle = -90
    angle = start_angle
    SLICE_ANGLE = 360 / 37
    total_spin_degrees = random.randint(1800, 2160)
    current_step = 20
    min_step = 1
    slowdown_factor = 0.99
    spinning = True

    while spinning:
        screen.fill((50, 50, 50))
        draw_wheel()
        draw_field()

        # Position berechnen
        rad = math.radians(angle % 360)
        ball_x = CENTER[0] + scaled_ball_radius * math.cos(rad)
        ball_y = CENTER[1] + scaled_ball_radius * math.sin(rad)

        # Ballgröße anpassen (z. B. 12 px bei Höhe 900)
        ball_radius = int((HEIGHT / 900) * 12)
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

        pygame.display.flip()
        clock.tick(60)

        angle += current_step
        if current_step > min_step:
            current_step *= slowdown_factor

        if angle - start_angle >= total_spin_degrees:
            spinning = False

    # Ergebnis berechnen
    global ball_position, ball_visible, last_result

    final_angle = angle % 360
    adjusted_angle = (final_angle + 95) % 360  # Korrektur je nach Startwinkel / Ausrichtung
    index = int(adjusted_angle // SLICE_ANGLE)
    result = numbers[index]

    ball_position = (int(ball_x), int(ball_y))  # speichere Ballposition
    last_result = result
    ball_visible = True  # Ball soll nun angezeigt bleiben

    print(result)
    if result == 0:
        print("ZERO")
    else:
        if result % 2 == 0:
            print("EVEN")
        else:
            print("ODD")

        def is_red(n): return n in {
            1, 3, 5, 7, 9, 12, 14, 16, 18,
            19, 21, 23, 25, 27, 30, 32, 34, 36
        }

        def is_2(n): return n in {
            2, 5, 8, 11, 14, 17, 20, 23,
            26, 29, 32, 35
        }

        print("RED" if is_red(result) else "BLACK")

        if 1 <= result <= 18:
            print("1 to 18")
        elif 19 <= result <= 36:
            print("19 to 36")

        if 1 <= result <= 12:
            print("1st 12")
        elif 13 <= result <= 24:
            print("2nd 12")
        elif 25 <= result <= 36:
            print("3rd 12")

        if result % 3 == 0:
            print("3rd Row")
        elif is_2(result):
            print("2nd Row")
        elif result != 0:
            print("1st Row")


    def calculator():
        num0 = 0

        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        num6 = 0
        num7 = 0
        num8 = 0
        num9 = 0
        num10 = 0
        num11 = 0
        num12 = 0
        num13 = 0
        num14 = 0
        num15 = 0
        num16 = 0
        num17 = 0
        num18 = 0
        num19 = 0
        num20 = 0
        num21 = 0
        num22 = 0
        num23 = 0
        num24 = 0
        num25 = 0
        num26 = 0
        num27 = 0
        num28 = 0
        num29 = 0
        num30 = 0
        num31 = 0
        num32 = 0
        num33 = 0
        num34 = 0
        num35 = 0
        num36 = 0

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

        if num0 == 1 and result == 0:
            print("Du hast auf 0 gesetzt und gewonnen!")

        if num1 == 1 and result == 1:
            print("Du hast auf 1 gesetzt und gewonnen!")

        if num2 == 1 and result == 2:
            print("Du hast auf 2 gesetzt und gewonnen!")

        if num3 == 1 and result == 3:
            print("Du hast auf 3 gesetzt und gewonnen!")

        if num4 == 1 and result == 4:
            print("Du hast auf 4 gesetzt und gewonnen!")

        if num5 == 1 and result == 5:
            print("Du hast auf 5 gesetzt und gewonnen!")

        if num6 == 1 and result == 6:
            print("Du hast auf 6 gesetzt und gewonnen!")

        if num7 == 1 and result == 7:
            print("Du hast auf 7 gesetzt und gewonnen!")

        if num8 == 1 and result == 8:
            print("Du hast auf 8 gesetzt und gewonnen!")

        if num9 == 1 and result == 9:
            print("Du hast auf 9 gesetzt und gewonnen!")

        if num10 == 1 and result == 10:
            print("Du hast auf 10 gesetzt und gewonnen!")

        if num11 == 1 and result == 11:
            print("Du hast auf 11 gesetzt und gewonnen!")

        if num12 == 1 and result == 12:
            print("Du hast auf 12 gesetzt und gewonnen!")

        if num13 == 1 and result == 13:
            print("Du hast auf 13 gesetzt und gewonnen!")

        if num14 == 1 and result == 14:
            print("Du hast auf 14 gesetzt und gewonnen!")

        if num15 == 1 and result == 15:
            print("Du hast auf 15 gesetzt und gewonnen!")

        if num16 == 1 and result == 16:
            print("Du hast auf 16 gesetzt und gewonnen!")

        if num17 == 1 and result == 17:
            print("Du hast auf 17 gesetzt und gewonnen!")

        if num18 == 1 and result == 18:
            print("Du hast auf 18 gesetzt und gewonnen!")

        if num19 == 1 and result == 19:
            print("Du hast auf 19 gesetzt und gewonnen!")

        if num20 == 1 and result == 20:
            print("Du hast auf 20 gesetzt und gewonnen!")

        if num21 == 1 and result == 21:
            print("Du hast auf 21 gesetzt und gewonnen!")

        if num22 == 1 and result == 22:
            print("Du hast auf 22 gesetzt und gewonnen!")

        if num23 == 1 and result == 23:
            print("Du hast auf 23 gesetzt und gewonnen!")

        if num24 == 1 and result == 24:
            print("Du hast auf 24 gesetzt und gewonnen!")

        if num25 == 1 and result == 25:
            print("Du hast auf 25 gesetzt und gewonnen!")

        if num26 == 1 and result == 26:
            print("Du hast auf 26 gesetzt und gewonnen!")

        if num27 == 1 and result == 27:
            print("Du hast auf 27 gesetzt und gewonnen!")

        if num28 == 1 and result == 28:
            print("Du hast auf 28 gesetzt und gewonnen!")

        if num29 == 1 and result == 29:
            print("Du hast auf 29 gesetzt und gewonnen!")

        if num30 == 1 and result == 30:
            print("Du hast auf 30 gesetzt und gewonnen!")

        if num31 == 1 and result == 31:
            print("Du hast auf 31 gesetzt und gewonnen!")

        if num32 == 1 and result == 32:
            print("Du hast auf 32 gesetzt und gewonnen!")

        if num33 == 1 and result == 33:
            print("Du hast auf 33 gesetzt und gewonnen!")

        if num34 == 1 and result == 34:
            print("Du hast auf 34 gesetzt und gewonnen!")

        if num35 == 1 and result == 35:
            print("Du hast auf 35 gesetzt und gewonnen!")

        if num36 == 1 and result == 36:
            print("Du hast auf 36 gesetzt und gewonnen!")

        if red == 1 and is_red(result):
            print("Du hast auf Rot gesetzt und gewonnen!")
        elif black == 1:
            print("Du hast auf Schwarz gesetzt und gewonnen!")

        if even == 1 and result % 2 == 0:
            print("Du hast auf Gerade gesetzt und gewonnen!")
        elif odd == 1:
            print("Du hast auf Ungerade gesetzt und gewonnen!")

        if  one_to_eighteen == 1 and 1 <= result <= 18:
            print("Du hast auf 1 zu 18 gesetzt und gewonnen!")
        elif nineteen_to_thirtysix == 1 and 19 <= result <= 36:
            print("Du hast auf 19 zu 36 gesetzt und gewonnen!")

        if one_to_twelve == 1 and 1 <= result <= 12:
            print("Du hast auf 1 zu 12 gesetzt und gewonnen!")
        elif thirteen_to_twentyfour == 1 and 13 <= result <= 24:
            print("Du hast auf 13 zu 24 gesetzt und gewonnen!")
        elif twentyfive_to_thirtysix == 1 and 25 <= result <= 36:
            print("Du hast auf 25 zu 36 gesetzt und gewonnen!")

        if rd_row == 1 and result % 3 == 0:
            print("Du hast auf die dritte Reihe gesetzt und gewonnen!")
        elif nd_row == 1 and is_2(result):
            print("Du hast auf die zweite Reihe gesetzt und gewonnen!")
        elif st_row == 1 and result != 0:
            print("Du hast auf erste Reihe gesetzt und gewonnen!")

    calculator()

from Casino.Bank.Scripts.chip import Chip
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # oder feste Größe
screen_size = screen.get_size()
chip = Chip("../../Bank/Data/Chip5.png", (400, 300), screen_size)

# Wenn du die Fenstergröße änderst:
new_size = screen.get_size()
chip.update_radius(new_size)



# === Spielschleife ===
running = True
while running and coins > 0:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                ball_visible = False
                ball_position = None
                last_result = None
                random_number()

    screen.fill((50, 50, 50))
    draw_wheel()
    draw_field()
    chip.handle_event(event)
    chip.draw(screen)
    if ball_visible and ball_position:
        pygame.draw.circle(screen, (255, 255, 255), ball_position, 12)
    pygame.display.flip()


print("Thanks for playing!")
pygame.quit()
sys.exit()