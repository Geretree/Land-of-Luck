import pygame
import random
import sys
import math
import json

# Farbengehens
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (215, 162, 20)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)

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

lever_angle = -45  # Hebel ruht leicht schräg
lever_pulled = False


def draw_housing():
    # Gehäuse
    pygame.draw.rect(screen, GOLD, (*HOUSING_POS, HOUSING_WIDTH, HOUSING_HEIGHT), border_radius=30)
    # Innenrahmen
    inner = pygame.Rect(HOUSING_POS[0] + 10, HOUSING_POS[1] + 10,
                        HOUSING_WIDTH - 20, HOUSING_HEIGHT - 20)
    pygame.draw.rect(screen, DARK_GRAY, inner, border_radius=20)


def draw_reels(values):
    for i, val in enumerate(values):
        x = REEL_X_START + i * (REEL_WIDTH + REEL_GAP)
        reel = pygame.Rect(x, REEL_Y, REEL_WIDTH, REEL_HEIGHT)
        pygame.draw.rect(screen, WHITE, reel, border_radius=15)
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
    global lever_angle, lever_pulled
    lever_angle = 30
    lever_pulled = True
    pygame.time.delay(150)
    lever_angle = -45
    return [random.randint(1, 7) for _ in range(REEL_COUNT)]


def load_coins():
    try:
        with open("../../Bank/Data/coin.json", "r") as f:
            daten = json.load(f)
        coins = daten["coin"]
    except FileNotFoundError:
        coins = 100
        daten = {"coin": coins}
    return coins, daten


def save_coins(coins, daten):
    with open("../../Bank/Data/coin.json", "w") as f:
        daten["coin"] = coins
        json.dump(daten, f)


def main():
    global lever_pulled
    coins, daten = load_coins()

    reels = ["-", "-", "-"]
    running = True
    while running and coins > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not lever_pulled:
                    reels = play_spin()
                    lever_pulled = False
                    # Adjust coin count based on spin result
                    if reels.count(reels[0]) == REEL_COUNT:  # Simple win condition
                        coins += 10
                    else:
                        coins -= 1

        # Update the game screen
        screen.fill(DARK_GRAY)
        draw_housing()
        draw_reels(reels)
        draw_lever()
        pygame.display.flip()
        clock.tick(60)

    save_coins(coins, daten)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
