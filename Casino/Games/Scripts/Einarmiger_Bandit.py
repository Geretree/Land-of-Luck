import pygame
import random
import json
import math
import sys

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
CENTER = (WIDTH // 2, HEIGHT // 2)
pygame.display.set_caption("Einarmiger Bandit")
clock = pygame.time.Clock()

# Lade Coins
try:
    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    coins = daten["coin"]
except FileNotFoundError:
    coins = 100
    daten = {"coin": coins}

def slot_machine():
    # Beispiel: Ein mittleres Rechteck als Slot-Kasten
    rect_width, rect_height = 300, 500
    rect_x = CENTER[0] - rect_width // 2
    rect_y = CENTER[1] - rect_height // 2
    pygame.draw.rect(screen, GOLD, (rect_x, rect_y, rect_width, rect_height), border_radius=20)

def draw_field():
    # Hintergrund grau füllen
    screen.fill((50, 50, 50))
    # Slot-Maschine zeichnen
    slot_machine()

def play():
    #Der Eigenliche Spielbegin

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
                play()

running = True
while running and coins > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_field()
    pygame.display.flip()
    clock.tick(60)  # FPS-Limit

# Coins speichern beim Beenden
with open("../../Bank/Data/coin.json", "w") as f:
    json.dump({"coin": coins}, f)

print("Thanks for playing!")
pygame.quit()
sys.exit()
