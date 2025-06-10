import json
import pygame
import sys
import os
import subprocess
from tkinter import messagebox

BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (230, 230, 230)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Füge den Projektroot-Pfad hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# Pfad zum Update-Skript
UPDATE_SCRIPT_PATH = os.path.join(project_root, "Casino", "User", "Data", "InsertIntoDatabase.py")


# Funktion zum Updaten der User Daten
def start_update_script():
    """Startet das Update-Skript als separater Prozess."""
    try:
        # Prüfe, ob das Update-Skript existiert
        if not os.path.exists(UPDATE_SCRIPT_PATH):
            print(f"Fehler: Update-Skript nicht gefunden: {UPDATE_SCRIPT_PATH}")
            return

        # Starte das Update-Skript als separater Prozess
        subprocess.Popen([sys.executable, UPDATE_SCRIPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Update-Skript wurde im Hintergrund gestartet.")
    except Exception as e:
        print(f"Fehler beim Starten des Update-Skripts: {str(e)}")

WIDTH, HEIGHT = screen.get_size()
CENTER = (WIDTH // 2, HEIGHT // 2)
X_SCALE = WIDTH / 1920
Y_SCALE = HEIGHT / 1080

with open("../../Bank/Data/coin.json", "r") as f:
    daten = json.load(f)

coins = daten["coin"]

# Auslesen der chips
def get_chip_counts(daten):
    keys = ["chip5_chips", "chip10_chips", "chip50_chips", "chip100_chips", "chip500_chips", "chip1000_chips", "chip5000_chips"]
    return [daten.get(key, 0) for key in keys]

# Speichern der chips
def save_chip_counts(daten, chip_counts):
    keys = ["chip5_chips", "chip10_chips", "chip50_chips", "chip100_chips", "chip500_chips", "chip1000_chips", "chip5000_chips"]
    for i, key in enumerate(keys):
        daten[key] = chip_counts[i]

chip_counts = get_chip_counts(daten)

def draw_background():
    rect_width = WIDTH * 0.05
    rect_x = CENTER[0] - rect_width / 2
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
def coin_counter(coins):
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
                    start_update_script()
                    return


            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # EINMAL lesen
                with open("../../Bank/Data/coin.json", "r") as f:
                    daten = json.load(f)

                # Button: PLUS
                for rect, index in click_rects_plus:
                    if rect.collidepoint(mouse_pos) and daten["coin"] >= configs[index]["value"]:
                        chip_counts[index] += 1
                        daten["coin"] -= configs[index]["value"]

                # Button: TRANSFER
                for rect3, index in click_rects_transfer:
                    if rect3.collidepoint(mouse_pos) and daten["coin"] >= configs[index]["value"]:
                        amount = daten["coin"] // configs[index]["value"]
                        chip_counts[index] += amount
                        daten["coin"] -= amount * configs[index]["value"]

                # Button: MINUS
                for rect2, index in click_rects_minus:
                    if rect2.collidepoint(mouse_pos) and chip_counts[index] > 0:
                        chip_counts[index] -= 1
                        daten["coin"] += configs[index]["value"]

                # Button: RESET
                for rect4, index in click_rects_reset:
                    if rect4.collidepoint(mouse_pos) and chip_counts[index] > 0:
                        amount = chip_counts[index]
                        daten["coin"] += amount * configs[index]["value"]
                        chip_counts[index] = 0

                # Chips speichern
                save_chip_counts(daten, chip_counts)

                # Coins speichern
                with open("../../Bank/Data/coin.json", "w") as f:
                    json.dump(daten, f, indent=4)

        configs = ChipData.chip_configs()
        screen.fill(WHITE)
        draw_background()
        coin_counter(daten["coin"])


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