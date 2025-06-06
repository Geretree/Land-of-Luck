from itertools import count
from pickle import GLOBAL
import json
import pygame
import sys


BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (230, 230, 230)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

WIDTH, HEIGHT = screen.get_size()
CENTER = (WIDTH // 2, HEIGHT // 2)
X_SCALE = WIDTH / 1920
Y_SCALE = HEIGHT / 1080

with open("../../Bank/Data/coin.json", "r") as f:
    daten = json.load(f)

coins = daten["coin"]
chip_counts = daten.get("chip_counts", [0] * 7)

def draw_background():
    rect_width = WIDTH * 0.05
    rect_height = HEIGHT * 0.05
    rect_x = CENTER[0] - rect_width / 2
    rect_y = CENTER[1] - rect_height / 2
    font = pygame.font.SysFont(None, int(60 * Y_SCALE))

    j = 90

    x = (rect_x * X_SCALE) + 130
    y = j * Y_SCALE
    w = 100 * X_SCALE
    h = 100 * Y_SCALE
    click_rects_plus = []
    click_rects_minus = []
    click_rects_transfer = []
    click_rects_reset = []

    configs = ChipData.chip_configs()


    for i in range(7):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, GREEN, (x, y, w, h))
        text_surface = font.render("+", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
        click_rects_plus.append((rect, i))

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90

    y = j * Y_SCALE
    x -= 260
    for i in range(7):
        rect4 = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, WHITE, (x, y, w, h))
        text_surface = font.render("X", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))  # zentrieren
        screen.blit(text_surface, text_rect)
        click_rects_reset.append((rect4, i))

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90

    y = j * Y_SCALE
    x += 130
    for i in range(7):
        rect2 = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, RED, (x, y, w, h))
        text_surface = font.render("-", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))  # zentrieren
        screen.blit(text_surface, text_rect)
        click_rects_minus.append((rect2, i))

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90

    y = j * Y_SCALE
    x += 260
    for i in range(7):
        rect3 = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, WHITE, (x, y, w, h))
        text_surface = font.render("->", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))  # zentrieren
        click_rects_transfer.append((rect3, i))

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90


    y = j * Y_SCALE
    x += 130
    for i in range(7):
        count = str(configs[i]["count"])
        rect = pygame.Rect(x, y, w + 200, h)
        pygame.draw.rect(screen, BLACK, rect)
        text_surface = font.render(count, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)

        y += 90


    return click_rects_plus, click_rects_minus, click_rects_transfer, click_rects_reset
def coin_counter():
    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)
    coins = daten["coin"]

    font = pygame.font.SysFont(None, int(36 * Y_SCALE))
    screen.blit(font.render(f"Coins: {coins}" , True, BLACK), (100,100))

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = True
    with open("../../Bank/Data/coin.json", "r") as f:
        daten = json.load(f)

    click_rects_plus, click_rects_minus, click_rects_transfer, click_rects_reset= draw_background()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC zum Beenden
                    daten["chip_counts"] = chip_counts

                    with open("../../Bank/Data/coin.json", "w") as f:
                        json.dump(daten, f, indent=4)
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for rect, index in click_rects_plus:
                    if rect.collidepoint(mouse_pos) and daten["coin"] > 0:
                        with open("../../Bank/Data/coin.json", "r") as f:
                            daten = json.load(f)

                        if coins // configs[index]["value"] >= 1:
                            chip_counts[index] += 1
                            daten["coin"] -= configs[index]["value"]

                        with open("../../Bank/Data/coin.json", "w") as f:
                            json.dump(daten, f, indent=4)

                for rect3, index in click_rects_transfer:
                    if rect3.collidepoint(mouse_pos) and daten["coin"] > 0:
                        with open("../../Bank/Data/coin.json", "r") as f:
                            daten = json.load(f)

                        amount = coins // configs[index]["value"]  # ganze Anzahl Chips
                        chip_counts[index] += amount
                        daten["coin"] -= amount * configs[index]["value"]

                        with open("../../Bank/Data/coin.json", "w") as f:
                            json.dump(daten, f, indent=4)

                for rect2, index in click_rects_minus:
                    if rect2.collidepoint(mouse_pos) and chip_counts[index] > 0:
                        with open("../../Bank/Data/coin.json", "r") as f:
                            daten = json.load(f)

                        chip_counts[index] -= 1
                        daten["coin"] += configs[index]["value"]

                        with open("../../Bank/Data/coin.json", "w") as f:
                            json.dump(daten, f, indent=4)

                for rect4, index in click_rects_reset:
                    if rect4.collidepoint(mouse_pos) and chip_counts[index] > 0:
                        with open("../../Bank/Data/coin.json", "r") as f:
                            daten = json.load(f)

                        value_per_chip = configs[index]["value"]
                        chip_amount = chip_counts[index]
                        refund = chip_amount * value_per_chip

                        # Rückerstatten und Chips zurücksetzen
                        daten["coin"] += refund
                        chip_counts[index] = 0
                        daten["chip_counts"] = chip_counts

                        with open("../../Bank/Data/coin.json", "w") as f:
                            json.dump(daten, f, indent=4)

        configs = ChipData.chip_configs()
        screen.fill(WHITE)
        draw_background()
        coin_counter()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



class ChipData:
    chip5_chips = []
    chip10_chips = []
    chip50_chips = []
    chip100_chips = []
    chip500_chips = []
    chip1000_chips = []
    chip5000_chips = []

    @staticmethod
    def get_all_chips():
        return (
            ChipData.chip5_chips +
            ChipData.chip10_chips +
            ChipData.chip50_chips +
            ChipData.chip100_chips +
            ChipData.chip500_chips +
            ChipData.chip1000_chips +
            ChipData.chip5000_chips
        )

    @staticmethod
    def chip_configs():
        return [
            {"value": 5, "count": chip_counts[0], "list": ChipData.chip5_chips},
            {"value": 10, "count": chip_counts[1], "list": ChipData.chip10_chips},
            {"value": 50, "count": chip_counts[2], "list": ChipData.chip50_chips},
            {"value": 100, "count": chip_counts[3], "list": ChipData.chip100_chips},
            {"value": 500, "count": chip_counts[4], "list": ChipData.chip500_chips},
            {"value": 1000, "count": chip_counts[5], "list": ChipData.chip1000_chips},
            {"value": 5000, "count": chip_counts[6], "list": ChipData.chip5000_chips}
        ]
if __name__ == "__main__":
    main()