import pygame
import random


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
        (130, 130),
        (x + card_width - 30, y + card_height - 30),
        (x + card_width - 30, 130),
        (130, y + card_height - 30)
    ]



    def Ecke(center_x, center_y, size=30):
        half = size // 2
        points = [
            (center_x, center_y - half - 5),  # oben
            (center_x + half, center_y),  # rechts
            (center_x, center_y + half + 5),  # unten
            (center_x - half, center_y)  # links
        ]
        pygame.draw.polygon(screen, RED, points)



    for center in mittelpunkte:
        Ecke(*center)  # *center entpackt (x, y)


# Hauptloop
running = True
while running:
    screen.fill(GREEN)  # Hintergrundfarbe

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Karte zeichnen
    pygame.draw.rect(screen, WHITE, card_rect)
    pygame.draw.rect(screen, BLACK, card_rect, 2)  # schwarzer Rahmen
    generate_card()
    pygame.display.flip()

pygame.quit()
