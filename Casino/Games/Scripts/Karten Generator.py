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



def Form():
    pygame.draw.circle(screen, BLACK, (x + 30, y + 30), 10)
    pygame.draw.circle(screen, BLACK, (x + 40, y + 20), 10)
    pygame.draw.circle(screen, BLACK, (x + 50, y + 30), 10)
    pygame.draw.polygon(screen, BLACK, [
        (x+38, y+20),
        (x+42, y+20),
        (x+42, y+50),
        (x+38, y+50)
    ])
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
    Form()
    pygame.display.flip()

pygame.quit()
