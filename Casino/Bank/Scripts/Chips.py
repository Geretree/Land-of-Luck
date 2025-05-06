import pygame

# Initialisiere Pygame
pygame.init()

# Setze den Bildschirm auf Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Lade das Chip-Bild
Chip5_img = pygame.image.load("../../../Assets/Chip5.png").convert_alpha()

# Bestimme die Position des Chips (Mitte des Bildschirms)
chip_rect = Chip5_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Spiel-Schleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False



    # Fülle den Bildschirm mit einer Farbe (z.B. schwarz)
    screen.fill((0, 0, 0))

    # Zeichne das Chip-Bild
    screen.blit(Chip5_img, chip_rect)

    # Aktualisiere den Bildschirm
    pygame.display.flip()

# Beende Pygame
pygame.quit()
