import pygame
import json
import os
from Casino.Games.Scripts.Karten_Generator import draw_card
from Casino.Bank.Scripts.Bank import ChipData
from Casino.Bank.Scripts.chip import Chips

# Pygame initialisieren und Vollbild starten
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Casino Lobby")

# Farben
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (255, 255, 255)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

# Statische Kartengrößen
CARD_WIDTH = 130 * 2
CARD_HEIGHT = 193 * 2
WIDTH, HEIGHT = screen.get_size()

# Globale Chip-Bild-Daten
chip_images = {}

def get_chip_counts(daten):
    keys = [
        "chip5_chips", "chip10_chips", "chip50_chips",
        "chip100_chips", "chip500_chips", "chip1000_chips", "chip5000_chips"
    ]
    return [daten.get(key, 0) for key in keys]


def draw_betting_pot(screen, width, height):
    center = (int(width * 0.89), int(height * 0.78))
    radius = int(height * 0.2)
    pygame.draw.circle(screen, WHITE, center, radius, 4)


def draw_card_place(screen, start_x, card_y, card_w, card_h, quarter):
    x = start_x
    for _ in range(4):
        rect = pygame.Rect(x - 4, card_y - 4, card_w, card_h)
        pygame.draw.rect(screen, WHITE, rect, 2)
        x += quarter

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

def spawn_all_chips(screen, screen_size):
    width, height = screen_size
    xpos = width * 0.5
    ypos_start = height * 0.85
    configs = ChipData.chip_configs()

    # Listen leeren
    for config in configs:
        config["list"].clear()

    # Lade Chip-Daten
    data_file = os.path.join(os.path.dirname(__file__), "..", "..", "Bank", "Data", "coin.json")
    with open(data_file, "r") as f:
        daten = json.load(f)

    chip_counts = get_chip_counts(daten)

    for index, config in enumerate(configs):
        value = config["value"]
        count = chip_counts[index]
        chip_list = config["list"]

        if value not in chip_images:
            image_path = os.path.join(os.path.dirname(__file__), "..", "..", "Bank", "Data", f"Chip{value}.png")
            chip_images[value] = pygame.image.load(image_path).convert_alpha()

        image = chip_images[value]

        for i in range(count):
            chip = Chips(image, (xpos, ypos_start - i), screen_size)
            chip.name = f"chip{value}_{i+1}"
            chip_list.append(chip)

        xpos += 0.06  # nächster Stapel


def main():
    # Bildschirmmaße und abhängige Konstanten
    width, height = screen.get_size()
    screen_size = (width, height)
    quarter_screen = width / 4.5
    card_y = height * 0.2
    card_start_x = quarter_screen - 252

    # Erste Zeichnungen
    screen.fill(GREEN)
    draw_betting_pot(screen, width, height)
    draw_card_place(screen, card_start_x, card_y, CARD_WIDTH, CARD_HEIGHT, quarter_screen)

    spawn_all_chips(screen, screen_size)
    all_chips = ChipData.get_all_chips()

    usses = 0
    x = card_start_x
    active_chip = None   # <==== FEHLTE BIS JETZT
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and usses < 4:
                    draw_card(screen, x, card_y)
                    x += quarter_screen
                    usses += 1
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

        # Optional: Hintergrund neu füllen
        # screen.fill(GREEN)

        # Chips zeichnen
        for chip in all_chips:
            chip.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
