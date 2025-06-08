# Casino/Lobby/Scripts/Lobby.py
import pygame
import traceback
import json
import sys
import os

# Fügen Sie den Projektroot-Pfad zum Systempfad hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

from Casino.Games.Scripts import Einarmiger_Bandit
from Casino.Games.Scripts import Roulette


# === Farben ===
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (45, 117, 16)
WHITE = (255, 255, 255)
BROWN = (156, 86, 12)
GOLD = (215, 162, 20)

try:
    with open("../../Bank/Data/spawnd_chips.json", "r") as f:
        daten = json.load(f)
    chips = daten["roulette_chips"]
except FileNotFoundError:
    chips = 100
    daten = {"roulette_chips": chips}


with open("../../Bank/Data/coin.json", "r") as f:
    daten = json.load(f)

daten["is_spawned"] = 0
with open("../../Bank/Data/coin.json", "w") as f:
    json.dump(daten, f, indent=4)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
win_width, win_height = pygame.display.get_surface().get_size()

# Spieler
peter_size = pygame.Vector2(60, 60)
peter_pos = pygame.Vector2()

# Bandit
bandit_size = pygame.Vector2(100, 100)
bandit_pos = pygame.Vector2(200, 200)

# Roulette
roulette_size = pygame.Vector2(200, 200)
roulette_pos = pygame.Vector2(200, 400)

#Save setzen
save_size = pygame.Vector2(100, 100)
save_pos = pygame.Vector2(400, 600)

# Assets laden mit ursprünglichen Pfaden
peter_image = pygame.image.load("../../Images/Happy_Man.png")
peter_image = pygame.transform.scale(peter_image, peter_size)

bandit_image = pygame.image.load("../../Images/bandit.png")
bandit_image = pygame.transform.scale(bandit_image, bandit_size)

roulette_image = pygame.image.load("../../Images/Roulette_table.png")
roulette_image = pygame.transform.scale(roulette_image, roulette_size)

save_image = pygame.image.load("../../Images/Speichern.png")
save_image = pygame.transform.scale(save_image, save_size)

running = True
dt = 0.0

# —————————————————————————————————————————————————————————————
# Spiel-Funktionen
# —————————————————————————————————————————————————————————————
def reset_game():
    global peter_pos
    peter_pos = pygame.Vector2(
        win_width/2 - peter_size.x/2,
        win_height/2 - peter_size.y/2
    )

def peter_player():
    global running, dt
    screen.blit(peter_image, (int(peter_pos.x), int(peter_pos.y)))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]: running = False
    speed = 300
    if keys[pygame.K_w]: peter_pos.y -= speed * dt
    if keys[pygame.K_s]: peter_pos.y += speed * dt
    if keys[pygame.K_a]: peter_pos.x -= speed * dt
    if keys[pygame.K_d]: peter_pos.x += speed * dt

    # Bildschirmgrenzen prüfen
    if (peter_pos.x < 0 or peter_pos.x + peter_size.x > win_width or
        peter_pos.y < 0 or peter_pos.y + peter_size.y > win_height):
        reset_game()


def spawn_bandit():
    screen.blit(bandit_image, bandit_pos)


def spawn_roulette():
    screen.blit(roulette_image, roulette_pos)

def spawn_save():
    screen.blit(save_image, save_pos)

def save_game():
    pass


def check_collision():
    global dt
    rect_p = pygame.Rect(peter_pos.x, peter_pos.y, *peter_size)
    rect_b = pygame.Rect(bandit_pos.x, bandit_pos.y, *bandit_size)
    rect_r = pygame.Rect(roulette_pos.x, roulette_pos.y, *roulette_size)
    rect_s = pygame.Rect(save_pos.x, save_pos.y + 200, *save_size)
    keys = pygame.key.get_pressed()

    if rect_p.colliderect(rect_b) and keys[pygame.K_SPACE]:
        Einarmiger_Bandit.main()

    if rect_p.colliderect(rect_r) and keys[pygame.K_SPACE]:
        Roulette.main()

    if rect_p.colliderect(rect_s) and keys[pygame.K_SPACE]:
        save_game()  # Rufe die Speicherfunktion auf


# —————————————————————————————————————————————————————————————
# Der asynchrone Game-Loop mit Debugging
# —————————————————————————————————————————————————————————————
def game():
    global running, dt
    # Sicherstellen, dass running True ist
    running = True
    reset_game()
    print("Game started, running initial:", running)
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Roter Hintergrund-Test zum Debuggen
            screen.fill(WHITE)
            spawn_bandit()
            spawn_roulette()
            spawn_save()
            peter_player()
            check_collision()

            pygame.display.flip()
            dt = clock.tick(60) / 1000.0


    except Exception:
        traceback.print_exc()
    finally:
        # Deaktiviert, damit Browser nicht sofort schließt
        # pygame.quit()
        print("Game exited")
        pygame.quit()

def main():
    game()

if __name__ == "__main__":
    main()