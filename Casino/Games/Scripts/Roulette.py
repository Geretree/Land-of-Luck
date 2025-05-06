import pygame
import random
import json
import math
import sys

# === Konfiguration ===
RADIUS = 300
SLICE_ANGLE = 360 / 37

# Farben
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
CENTER = (400, HEIGHT // 2)
pygame.display.set_caption("Roulette")
clock = pygame.time.Clock()

# Lade Coins
try:
    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    coins = daten["coin"]
except FileNotFoundError:
    coins = 100
    daten = {"coin": coins}

# Liste der Roulette-Zahlen (im französischen Format)
numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0
]

def draw_wheel():
    pygame.draw.circle(screen, BROWN, CENTER, 360)
    pygame.draw.circle(screen, GOLD, CENTER, 310)
    green_index = 37
    start_angle = -95 - SLICE_ANGLE * green_index
    angle = start_angle

    # Außenbereiche (Farbfelder)
    for i in range(38):
        color = GREEN if i == 37 else RED if i % 2 else BLACK
        draw_slice(angle, color, i)
        angle += SLICE_ANGLE

    # Mitte zeichnen
    pygame.draw.circle(screen, GOLD, CENTER, 255)
    pygame.draw.circle(screen, GREEN, CENTER, 245)
    pygame.draw.circle(screen, GOLD, CENTER, 205)
    pygame.draw.circle(screen, BROWN, CENTER, 195)
    pygame.draw.circle(screen, GOLD, CENTER, 50)

    # Gold-Markierungen aussen
    angle = start_angle  # Zurücksetzen!
    for i in range(38):
        draw_Edge(angle)
        angle += SLICE_ANGLE

    # Gold-Markierungen innen
    angle = start_angle  # Zurücksetzen!
    for i in range(4):
        draw_Middle(angle)
        angle += 90

    # Gold-Markierungen innen punkte
    angle = start_angle  # Zurücksetzen!
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

    # Die Zahl auf jedem Slice anzeigen
    a = math.radians(angle + SLICE_ANGLE / 2)
    x = CENTER[0] + (RADIUS - 25) * math.cos(a)
    y = CENTER[1] + (RADIUS - 25) * math.sin(a)
    font = pygame.font.SysFont("arial", 20)
    text = font.render(str(numbers[index]), True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def draw_Edge(angle):
    a = math.radians((angle + 5) + SLICE_ANGLE / 2)
    x1 = CENTER[0] + 300 * math.cos(a)
    y1 = CENTER[1] + 300 * math.sin(a)
    x2 = CENTER[0] + 200 * math.cos(a)
    y2 = CENTER[1] + 200 * math.sin(a)
    pygame.draw.line(screen, GOLD, (x1, y1), (x2, y2), 4)

def draw_Middle(angle):
    a = math.radians(angle + SLICE_ANGLE / 2)
    x1 = CENTER[0] + 0 * math.cos(a)
    y1 = CENTER[1] + 0 * math.sin(a)
    x2 = CENTER[0] + 160 * math.cos(a)
    y2 = CENTER[1] + 160 * math.sin(a)
    pygame.draw.line(screen, GOLD, (x1, y1), (x2, y2), 10)

def draw_Points(angle):
    a = math.radians(angle + SLICE_ANGLE / 2)
    x1 = CENTER[0] + 160 * math.cos(a)
    y1 = CENTER[1] + 160 * math.sin(a)
    pygame.draw.circle(screen, GOLD, (x1, y1), 20)





#---------------------------------------Fläche----------------------------------------------

def draw_field():
    pygame.draw.line(screen, WHITE, (850, 100), (1900, 100), 10)
    pygame.draw.line(screen, WHITE, (925, 200), (1900, 200), 10)
    pygame.draw.line(screen, WHITE, (925, 300), (1900, 300), 10)
    pygame.draw.line(screen, WHITE, (850, 400), (1900, 400), 10)
    pygame.draw.line(screen, WHITE, (925, 500), (1825, 500), 10)
    pygame.draw.line(screen, WHITE, (925, 600), (1825, 600), 10)
    pygame.draw.line(screen, WHITE, (850, 100), (800, 250), 10)
    pygame.draw.line(screen, WHITE, (850, 400), (800, 250), 10)
    leng = 925
    for i in range(14):
        pygame.draw.line(screen, WHITE, (leng, 96), (leng, 405), 10)
        leng += 75
    leng = 925
    for i in range(4):
        pygame.draw.line(screen, WHITE, (leng, 396), (leng, 505), 10)
        leng += 300
    leng = 925
    for i in range(7):
        pygame.draw.line(screen, WHITE, (leng, 496), (leng, 605), 10)
        leng += 150

    font = pygame.font.SysFont(None, 36)

    labels = ["1st 12", "2nd 12", "3rd 12"]

    for i, x in enumerate([945, 1245, 1545]):
        pygame.draw.rect(screen, GOLD, (x, 420, 260, 60))
        pygame.draw.rect(screen, GREEN, (x + 2, 422, 256, 56))

        # Text vorbereiten
        text = font.render(labels[i], True, WHITE)
        text_rect = text.get_rect(center=(x + 130, 450))  # 130 = Hälfte der Breite (260/2), 450 = Mitte der Höhe
        screen.blit(text, text_rect)

    labels = ["1 to 18", "EVEN", "ODD", "19 to 36"]

    for i, x in enumerate([945, 1095, 1545, 1695]):
        pygame.draw.rect(screen, GOLD, (x, 520, 110, 60))
        pygame.draw.rect(screen, GREEN, (x + 2, 522, 106, 56))

        # Text vorbereiten
        text = font.render(labels[i], True, WHITE)
        text_rect = text.get_rect(center=(x + 55, 550))  # 130 = Hälfte der Breite (260/2), 450 = Mitte der Höhe
        screen.blit(text, text_rect)



    font = pygame.font.SysFont(None, 18)
    labels = ["2to1", "2to1", "2to1"]

    for i, y in enumerate([120, 220, 320]):
        pygame.draw.rect(screen, GOLD, (1845, y, 35, 60))
        pygame.draw.rect(screen, GREEN, (1847, y + 2, 31, 56))

        # Text mittig im grünen Feld platzieren
        text = font.render(labels[i], True, WHITE)
        text_rect = text.get_rect(center=(1845 + 35 // 2, y + 60 // 2))
        screen.blit(text, text_rect)

    font = pygame.font.SysFont(None, 36)

    def draw_diamond(x, y, size1, size2, color):
        pygame.draw.polygon(screen, color, [
            (x, y - size1),
            (x + size2, y),
            (x, y + size1),
            (x - size2, y)
        ])

    # Diamanten mit Schichten
    diamonds = [
        (1300, 550, 40, 60, GOLD),
        (1300, 550, 38, 58, RED),
        (1450, 550, 40, 60, GOLD),
        (1450, 550, 38, 58, BLACK),
    ]

    for x, y, size1, size2, color in diamonds:
        draw_diamond(x, y, size1, size2, color)

    pygame.draw.ellipse(screen, GOLD, (838, 208, 59, 84))
    pygame.draw.ellipse(screen, GREEN, (840, 210, 55, 80))

    text = font.render("0", True, WHITE)
    screen.blit(text, (860, 240))


    def draw_color(color, x, y, number):
        pygame.draw.ellipse(screen, color, (x, y, 55, 80))
        text = font.render(str(number), True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + 27, y + 40))
        screen.blit(text, text_rect)

    # Farben in Zeilen
    rows = [
        [RED, BLACK, RED, BLACK, BLACK, RED, RED, BLACK, RED, BLACK, BLACK, RED],
        [BLACK, RED, BLACK, BLACK, RED, BLACK, BLACK, RED, BLACK, BLACK, RED, BLACK],
        [RED, BLACK, RED, RED, BLACK, RED, RED, BLACK, RED, RED, BLACK, RED]
    ]

    posx_start = 935
    posy_start = 310
    rows_count = len(rows)
    cols_count = len(rows[0])

    # Zahlen von oben nach unten (Zeile 0 = oben)
    numbers = [[0 for _ in range(cols_count)] for _ in range(rows_count)]
    n = 1
    for col in range(cols_count):
        for row in range(rows_count):  # <--- von oben nach unten
            numbers[row][col] = n
            n += 1

    # Zeichnen: zeilenweise
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

    radius = 225
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
        ball_x = CENTER[0] + radius * math.cos(rad)
        ball_y = CENTER[1] + radius * math.sin(rad)
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 12)

        pygame.display.flip()
        clock.tick(60)

        angle += current_step
        if current_step > min_step:
            current_step *= slowdown_factor

        if angle - start_angle >= total_spin_degrees:
            spinning = False

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
    color = 0

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

        print("Rot" if is_red(result) else "Schwarz")

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

        red = 1
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




# === Spielschleife ===
running = True
while running and coins > 0:
    for event in pygame.event.get():
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
    if ball_visible and ball_position:
        pygame.draw.circle(screen, (255, 255, 255), ball_position, 12)
    pygame.display.flip()

print("Thanks for playing!")
pygame.quit()
sys.exit()