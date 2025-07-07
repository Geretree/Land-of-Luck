import pygame
from Karten_Generator import draw_card  # Annahme: die Funktion liegt in 'deine_karte.py'
import json
from Casino.Bank.Scripts.Bank import ChipData
from Casino.Bank.Scripts.chip import Chips

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
running = True

def get_chip_counts(daten):
    keys = ["chip5_chips", "chip10_chips", "chip50_chips", "chip100_chips", "chip500_chips", "chip1000_chips", "chip5000_chips"]
    return [daten.get(key, 0) for key in keys]

BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (255, 255, 255)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

screen_size = screen.get_size()
screen.fill(GREEN)
usses = 0
quarterscreen = WIDTH / 4.5

card_width = 130 * 2
card_height = 193 * 2
y = HEIGHT * 0.2
x = quarterscreen - 252
h = quarterscreen - 252

all_chips = ChipData.get_all_chips()
config = ChipData.chip_configs()

def draw_betting_pot():
    pygame.draw.circle(screen, WHITE,(quarterscreen*4-126, HEIGHT*0.78), HEIGHT*0.2, 4)

def draw_card_place():
    rect_size = pygame.Rect(h - 4, y - 4, card_width, card_height)
    pygame.draw.rect(screen, WHITE, rect_size, 2)
def spawn_all_chips():
    global chip_images  # auf globale Variable zugreifen
    ypos = HEIGHT * 0.85
    xpos = WIDTH * 0.5
    orxpos = WIDTH * 0.5

    configs = ChipData.chip_configs()

    for config in configs:
        config["list"].clear()

    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    chip_counts = get_chip_counts(daten)

    for index, config in enumerate(configs):
        value = config["value"]
        count = chip_counts[index]
        chip_list = config["list"]
        image = chip_images[value]

        if value not in chip_images:
            chip_images[value] = pygame.image.load(f"../../Bank/Data/Chip{value}.png").convert_alpha()

        image = chip_images[value]
        namenumber = 1

        for i in range(count):
            chip = Chips(image, (xpos, ypos), screen_size)
            chip.name = f"chip{value}_{namenumber}"
            chip_list.append(chip)
            namenumber += 1
            ypos -= 1
        ypos = HEIGHT * 0.85
        xpos += 0.06




while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key == pygame.K_SPACE and usses < 4:
                draw_card(screen, x, y)
                x += quarterscreen
                usses += 1

    draw_betting_pot()
    h = quarterscreen - 252
    for i in range(4):
        draw_card_place()
        h += quarterscreen
    for chip in all_chips:
        chip.draw(screen)

    pygame.display.flip()

pygame.quit()
