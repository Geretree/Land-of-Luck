import pygame
import random
import sys
import math

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (215, 162, 20)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pygame Setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Einarmiger Bandit")
clock = pygame.time.Clock()

# Center
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Slot-Maschine Geometrie
HOUSING_WIDTH, HOUSING_HEIGHT = 400, 500
HOUSING_POS = (CENTER[0] - HOUSING_WIDTH // 2, CENTER[1] - HOUSING_HEIGHT // 2)

REEL_COUNT = 3
REEL_WIDTH, REEL_HEIGHT = 100, 150
REEL_GAP = 20
REEL_X_START = CENTER[0] - (REEL_COUNT * REEL_WIDTH + (REEL_COUNT - 1) * REEL_GAP) // 2
REEL_Y = CENTER[1] - REEL_HEIGHT // 2

font = pygame.font.Font(None, 80)

# Hebelsteuerung
lever_angle = 45
lever_pulled = False
spin_start_time = 0
SPIN_DURATION = 500  # Hebel bleibt 0.5s unten

# Spin-Sperre
spin_locked = False
spin_lock_time = 0
SPIN_LOCK_DURATION = 5000  # 5 Sekunden

def draw_housing():
    pygame.draw.rect(screen, GOLD, (*HOUSING_POS, HOUSING_WIDTH, HOUSING_HEIGHT), border_radius=30)
    inner = pygame.Rect(HOUSING_POS[0] + 10, HOUSING_POS[1] + 10,
                        HOUSING_WIDTH - 20, HOUSING_HEIGHT - 20)
    pygame.draw.rect(screen, DARK_GRAY, inner, border_radius=20)

def draw_reels(values, colors=None):
    if colors is None:
        colors = [WHITE] * len(values)
    for i, val in enumerate(values):
        x = REEL_X_START + i * (REEL_WIDTH + REEL_GAP)
        reel = pygame.Rect(x, REEL_Y, REEL_WIDTH, REEL_HEIGHT)
        pygame.draw.rect(screen, colors[i], reel, border_radius=15)
        pygame.draw.rect(screen, BLACK, reel, 4, border_radius=15)
        text = font.render(str(val), True, BLACK)
        txt_rect = text.get_rect(center=reel.center)
        screen.blit(text, txt_rect)

def draw_lever():
    base_x = HOUSING_POS[0] + HOUSING_WIDTH + 30
    base_y = CENTER[1] + 60
    length = 140
    angle = math.radians(lever_angle)
    end = (base_x + math.cos(angle) * length,
           base_y - math.sin(angle) * length)
    pygame.draw.line(screen, BROWN, (base_x, base_y), end, 12)
    pygame.draw.circle(screen, DARK_GRAY, (int(end[0]), int(end[1])), 18)
    pygame.draw.circle(screen, BLACK, (int(end[0]), int(end[1])), 20, 4)

def play_spin():
    return [random.randint(1, 7) for _ in range(REEL_COUNT)]

def detect_patterns(values):
    global spin_locked, spin_lock_time, now
    colors = [WHITE] * len(values)

    # Drei gleiche
    if values[0] == values[1] == values[2]:
        if values[0] == 7:
            spin_locked = True
            spin_lock_time = now
            return [RED] * 3
        else:
            return [GREEN] * 3

    # Reihenfolge
    if sorted(values) == list(range(min(values), max(values) + 1)):
        return [BLUE] * 3

    # Zwei gleiche
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                colors[i] = colors[j] = GOLD

    return colors

def main():
    global lever_pulled, lever_angle, spin_start_time, spin_locked, spin_lock_time

    reels = ["-", "-", "-"]
    colors = [WHITE] * 3
    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not lever_pulled and not spin_locked:
                    lever_pulled = True
                    spin_start_time = now
                    lever_angle = -45  # Hebel nach unten
                    reels = play_spin()
                    colors = detect_patterns(reels)

        # Hebel langsam zurück
        if lever_pulled and now - spin_start_time > SPIN_DURATION:
            lever_angle = 45
            lever_pulled = False

        # Spin-Sperre aufheben nach 5 Sekunden
        if spin_locked and now - spin_lock_time > SPIN_LOCK_DURATION:
            spin_locked = False

        screen.fill(DARK_GRAY)
        draw_housing()
        draw_reels(reels, colors)
        draw_lever()

        # Hinweis auf Wartezeit
        if spin_locked:
            wait_text = font.render("Warte...", True, BLUE)
            screen.blit(wait_text, (CENTER[0] - wait_text.get_width() // 2, REEL_Y + REEL_HEIGHT + 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
