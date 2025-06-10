import pygame
import random
import math


# Farben
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (255, 255, 255)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Jasskarte anzeigen")

# Jasskartengröße (z. B. 126 x 189 px)
card_width = 126 * 2
card_height = 189 * 2
x = 100
y = 100
card_rect = pygame.Rect(x, y, card_width, card_height)

def generate_card():
    mittelpunkte = [
        (x + (card_width * 0.1), y + (card_height * 0.1)),
        (x + (card_width * 0.1), y + (card_height * 0.9)),
        (x + (card_width * 0.9), y + (card_height * 0.1)),
        (x + (card_width * 0.9), y + (card_height * 0.9))
    ]

    posforone = [
        (x +(card_width/2),y +(card_height/2))
    ]
    posfortwo = [
        (x + (card_width / 2), y + (card_height * 0.15)),
        (x + (card_width / 2), y + (card_height * 0.85))
    ]
    posforthree = [
        (x + (card_width / 2), y + (card_height * 0.15)),
        (x + (card_width / 2), y + (card_height / 2)),
        (x + (card_width / 2), y + (card_height * 0.85))
    ]
    posforfour = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width * 0.7), y + (card_height * 0.85))
    ]
    posforfive = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width / 2), y + (card_height / 2)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width * 0.7), y + (card_height * 0.85))
    ]
    posforsix = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.3), y + (card_height / 2)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height / 2)),
        (x + (card_width * 0.7), y + (card_height * 0.85))
    ]
    posforseven = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.3), y + (card_height / 2)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width / 2), y + ((card_height * 0.85) - (card_height * 0.525))),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height / 2)),
        (x + (card_width * 0.7), y + (card_height * 0.85))
    ]
    posforeight = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.3), y + (card_height / 2)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width / 2), y + ((card_height * 0.85) - (card_height * 0.525))),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height / 2)),
        (x + (card_width * 0.7), y + (card_height * 0.85)),
        (x + (card_width / 2), y + ((card_height * 0.85) - (card_height * 0.175)))
    ]
    posfornine = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.3), y + (card_height * 0.38333)),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height * 0.38333)),
        (x + (card_width / 2), y + (card_height / 2)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width * 0.3), y + (card_height * 0.61666)),
        (x + (card_width * 0.7), y + (card_height * 0.85)),
        (x + (card_width * 0.7), y + (card_height * 0.61666))
    ]
    posforten = [
        (x + (card_width * 0.3), y + (card_height * 0.15)),
        (x + (card_width * 0.3), y + (card_height * 0.38333)),
        (x + (card_width * 0.7), y + (card_height * 0.15)),
        (x + (card_width * 0.7), y + (card_height * 0.38333)),
        (x + (card_width / 2), y + (card_height * 0.2625)),
        (x + (card_width / 2), y + (card_height * 0.7375)),
        (x + (card_width * 0.3), y + (card_height * 0.85)),
        (x + (card_width * 0.3), y + (card_height * 0.61666)),
        (x + (card_width * 0.7), y + (card_height * 0.85)),
        (x + (card_width * 0.7), y + (card_height * 0.61666))
    ]

    wahl = random.randint(1, 10)
    form = random.randint(1, 4)
    if wahl == 1:
        kartenzahl = posforone
    elif wahl == 2:
        kartenzahl = posfortwo
    elif wahl == 3:
        kartenzahl = posforthree
    elif wahl == 4:
        kartenzahl = posforfour
    elif wahl == 5:
        kartenzahl = posforfive
    elif wahl == 6:
        kartenzahl = posforsix
    elif wahl == 7:
        kartenzahl = posforseven
    elif wahl == 8:
        kartenzahl = posforeight
    elif wahl == 9:
        kartenzahl = posfornine
    elif wahl == 10:
        kartenzahl = posforten



    def Ecke(center_x, center_y):
        half = size // 2
        points = [
            (center_x, center_y - half - 5),  # oben
            (center_x + half, center_y),  # rechts
            (center_x, center_y + half + 5),  # unten
            (center_x - half, center_y)  # links
        ]
        pygame.draw.polygon(screen, RED, points)

    def Dreieck(center_x, center_y):
        half = size // 4
        points1 = [
            (center_x, center_y - half - 5),  # oben
            (center_x + half, center_y),  # rechts
            (center_x - half, center_y)  # links
        ]
        pygame.draw.polygon(screen, RED, points1)
        points2 = [
            (center_x + half, center_y - half - 5),  # oben
            (center_x + half + half, center_y),  # rechts
            (center_x, center_y)  # links
        ]
        pygame.draw.polygon(screen, RED, points2)
        points3 = [
            (center_x, center_y - half - 5),  # oben
            (center_x + half, center_y),  # rechts
            (center_x, center_y + half + 5),  # unten
            (center_x - half, center_y)  # links
        ]


    def Kreis(center_x, center_y):
        points = (center_x, center_y)  # Mitte
        pygame.draw.circle(screen, BLACK, points, (size / 2))

    form = random.randint(1, 3)
    if form == 1:
        formwahl = Ecke
    elif form == 2:
        formwahl = Dreieck
    elif form == 3:
        formwahl = Kreis

    for center in mittelpunkte:
        size = 30
        formwahl(*center)  # *center entpackt (x, y)

    for center in kartenzahl:
        size = 40
        formwahl(*center)  # *center entpackt (x, y)


# Hauptloop
screen.fill(GREEN)

running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Karte zeichnen
                pygame.draw.rect(screen, WHITE, card_rect)
                pygame.draw.rect(screen, BLACK, card_rect, 2)

                generate_card()

    # Hintergrund


    pygame.display.flip()

pygame.quit()
