import pygame


pygame.init()

# Bildschirm im Vollbildmodus
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

win_width, win_height = pygame.display.get_surface().get_size()

# Spielergröße
peter_size = pygame.Vector2(60, 60)
peter_pos = pygame.Vector2()  # Initialisierung, später gesetzt

# Bandit
bandit_size = pygame.Vector2(100, 100)
bandit_pos = pygame.Vector2(200, 200)

# Roulette
roulette_size = pygame.Vector2(200, 200)
roulette_pos = pygame.Vector2(200, 400)

# Bild einmal laden und skalieren
peter_image = pygame.image.load("../Images/Happy_Man.png")
peter_image = pygame.transform.scale(peter_image, peter_size)

bandit_image = pygame.image.load("../Images/bandit.png")
bandit_image = pygame.transform.scale(bandit_image, bandit_size)

roulette_image = pygame.image.load("../Images/Roulette_table.png")
roulette_image = pygame.transform.scale(roulette_image, roulette_size)

# Spielstatus
running = True
dt = 0

# Aktionen bei Kollisionen
def bandit():
    print("Peter hat den Banditen berührt!")
    from Casino.Games.Scripts import bandit
    bandit


def roulette():
    print("Peter hat das Roulette berührt!")
    from Casino.Games.Scripts import Roulette
    Roulette



# Spielerposition zurücksetzen
def reset_game():
    global peter_pos
    peter_pos = pygame.Vector2(win_width / 2 - peter_size.x / 2, win_height / 2 - peter_size.y / 2)

# Spielerbewegung und Zeichnung
def peter_player():
    screen.blit(peter_image, (int(peter_pos.x), int(peter_pos.y)))

    keys = pygame.key.get_pressed()
    speed = 300
    if keys[pygame.K_w]:
        peter_pos.y -= speed * dt
    if keys[pygame.K_s]:
        peter_pos.y += speed * dt
    if keys[pygame.K_a]:
        peter_pos.x -= speed * dt
    if keys[pygame.K_d]:
        peter_pos.x += speed * dt
    if keys[pygame.K_q]:
        global running
        running = False

    # Bildschirmgrenzen überprüfen
    if (peter_pos.y < 0 or peter_pos.y + peter_size.y > win_height or
            peter_pos.x < 0 or peter_pos.x + peter_size.x > win_width):
        reset_game()

# Gegner & Objekte zeichnen
def spawn_bandit():
    screen.blit(bandit_image, bandit_pos)

def spawn_roulette():
    screen.blit(roulette_image, roulette_pos)

# Kollisionserkennung
def check_collision():
    peter_rect = pygame.Rect(peter_pos.x, peter_pos.y, *peter_size)
    bandit_rect = pygame.Rect(bandit_pos.x, bandit_pos.y, *bandit_size)
    roulette_rect = pygame.Rect(roulette_pos.x, roulette_pos.y, *roulette_size)

    if peter_rect.colliderect(bandit_rect):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bandit()
            reset_game()

    if peter_rect.colliderect(roulette_rect):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            roulette()
            reset_game()

# Initialisierung
reset_game()

# Hauptspielschleife
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    spawn_bandit()
    spawn_roulette()
    peter_player()
    check_collision()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
