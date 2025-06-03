from itertools import count

import pygame
a = 1
b = 1
c = 1
d = 1
e = 1
f = 1
g = 1

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

    for i in range(7):
        pygame.draw.rect(screen, GREEN, (x, y, w, h))
        text_surface = font.render("+", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))  # zentrieren

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90

    y = j * Y_SCALE
    x -= 130
    for i in range(7):
        pygame.draw.rect(screen, RED, (x, y, w, h))
        text_surface = font.render("-", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))  # zentrieren

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90

    y = j * Y_SCALE
    x += 260
    for i in range(7):
        pygame.draw.rect(screen, WHITE, (x, y, w, h))
        text_surface = font.render("->", True, BLACK)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))  # zentrieren

        # Text anzeigen
        screen.blit(text_surface, text_rect)
        y += 90

    click_rects = []  # Liste speichern für spätere Prüfung

    y = j * Y_SCALE
    x += 130
    configs = ChipData.chip_configs()
    for i in range(7):
        count = str(configs[i]["count"])
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, BLACK, rect)
        text_surface = font.render(count, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)

        click_rects.append((rect, i))  # Speichere das Rechteck zusammen mit dem Index
        y += 90


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC zum Beenden
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Linksklick
                mouse_pos = pygame.mouse.get_pos()
                for rect, index in click_rects:
                    if rect.collidepoint(mouse_pos):
                        print(f"Feld {index} wurde angeklickt – Wert: {configs[index]['value']}")
                        # → Hier kannst du machen was du willst (z. B. Chips hinzufügen/entfernen)

        screen.fill(WHITE)
        draw_background()

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
            {"value": 5, "count": a, "list": ChipData.chip5_chips},
            {"value": 10, "count": b, "list": ChipData.chip10_chips},
            {"value": 50, "count": c, "list": ChipData.chip50_chips},
            {"value": 100, "count": d, "list": ChipData.chip100_chips},
            {"value": 500, "count": e, "list": ChipData.chip500_chips},
            {"value": 1000, "count": f, "list": ChipData.chip1000_chips},
            {"value": 5000, "count": g, "list": ChipData.chip5000_chips}
        ]
if __name__ == "__main__":
    main()