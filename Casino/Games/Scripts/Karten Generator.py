import pygame

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
card_width = 126
card_height = 189
card_rect = pygame.Rect(100, 100, card_width, card_height)

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

    pygame.display.flip()

pygame.quit()
