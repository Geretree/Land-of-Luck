import pygame
import random

BLACK = (0, 0, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# Kartenmaße (z.B. 252 x 378 px)
card_width = 126 * 2
card_height = 189 * 2

def draw_card(surface, x, y):
    card_rect = pygame.Rect(x, y, card_width, card_height)
    pygame.draw.rect(surface, WHITE, card_rect)
    pygame.draw.rect(surface, BLACK, card_rect, 2)

    mittelpunkte = [
        (x + (card_width * 0.1), y + (card_height * 0.1)),
        (x + (card_width * 0.1), y + (card_height * 0.9)),
        (x + (card_width * 0.9), y + (card_height * 0.1)),
        (x + (card_width * 0.9), y + (card_height * 0.9))
    ]

    posforone = [(x + card_width/2, y + card_height/2)]
    posfortwo = [(x + card_width/2, y + card_height*0.15),
                 (x + card_width/2, y + card_height*0.85)]
    posforthree = posfortwo + [posforone[0]]
    posforfour = [(x + card_width*0.3, y + card_height*0.15),
                  (x + card_width*0.7, y + card_height*0.15),
                  (x + card_width*0.3, y + card_height*0.85),
                  (x + card_width*0.7, y + card_height*0.85)]
    posforfive = posforfour[:2] + [posforone[0]] + posforfour[2:]
    posforsix = [(x + card_width*0.3, y + card_height*0.15),
                 (x + card_width*0.3, y + card_height/2),
                 (x + card_width*0.3, y + card_height*0.85),
                 (x + card_width*0.7, y + card_height*0.15),
                 (x + card_width*0.7, y + card_height/2),
                 (x + card_width*0.7, y + card_height*0.85)]
    posforseven = posforsix[:3] + [(x + card_width/2, y + card_height*0.325)] + posforsix[3:]
    posforeight = posforseven + [(x + card_width/2, y + card_height*0.675)]
    posfornine = [
        (x + card_width * 0.3, y + card_height * 0.15),
        (x + card_width * 0.3, y + card_height * 0.38333),
        (x + card_width * 0.7, y + card_height * 0.15),
        (x + card_width * 0.7, y + card_height * 0.38333),
        (x + card_width / 2, y + card_height / 2),
        (x + card_width * 0.3, y + card_height * 0.85),
        (x + card_width * 0.3, y + card_height * 0.61666),
        (x + card_width * 0.7, y + card_height * 0.85),
        (x + card_width * 0.7, y + card_height * 0.61666)
    ]
    posforten = [
        (x + card_width * 0.3, y + card_height * 0.15),
        (x + card_width * 0.3, y + card_height * 0.38333),
        (x + card_width * 0.7, y + card_height * 0.15),
        (x + card_width * 0.7, y + card_height * 0.38333),
        (x + card_width / 2, y + card_height * 0.2625),
        (x + card_width / 2, y + card_height * 0.7375),
        (x + card_width * 0.3, y + card_height * 0.85),
        (x + card_width * 0.3, y + card_height * 0.61666),
        (x + card_width * 0.7, y + card_height * 0.85),
        (x + card_width * 0.7, y + card_height * 0.61666)
    ]

    zahlen = {
        1: posforone,
        2: posfortwo,
        3: posforthree,
        4: posforfour,
        5: posforfive,
        6: posforsix,
        7: posforseven,
        8: posforeight,
        9: posfornine,
        10: posforten
    }

    def Ecke(cx, cy, size):
        offset = 0.05 * size
        half = size // 2
        pygame.draw.polygon(surface, RED, [
            (cx, cy - half - offset),
            (cx + half, cy),
            (cx, cy + half + offset),
            (cx - half, cy)
        ])

    def Herz(cx, cy, size):
        h = size // 4
        pygame.draw.circle(surface, RED, (cx - h, cy), h)
        pygame.draw.circle(surface, RED, (cx + h, cy), h)
        pygame.draw.polygon(surface, RED, [
            (cx + h*2, cy),
            (cx, cy + h*2.5),
            (cx - h*2, cy)
        ])

    def Schaufel(cx, cy, size):
        h = size // 4
        pygame.draw.circle(surface, BLACK, (cx - h, cy), h)
        pygame.draw.circle(surface, BLACK, (cx + h, cy), h)
        pygame.draw.polygon(surface, BLACK, [
            (cx + h*2, cy),
            (cx, cy - h*2.5),
            (cx - h*2, cy)
        ])
        pygame.draw.rect(surface, BLACK, (cx - size*0.02, cy, size*0.08, size*0.5))

    def Kreuz(cx, cy, size):
        r = size // 6
        offset = size // 4
        pygame.draw.circle(surface, BLACK, (cx - offset, cy), r)
        pygame.draw.circle(surface, BLACK, (cx + offset, cy), r)
        pygame.draw.circle(surface, BLACK, (cx, cy - offset), r)
        pygame.draw.rect(surface, BLACK, (cx - size * 0.035, cy - size* 0.2, size * 0.08, size * 0.6))
        pygame.draw.rect(surface, BLACK, (cx - size*0.25, cy - size*0.02, size*0.5, size*0.08))

    symbole = {1: Ecke, 2: Herz, 3: Schaufel, 4: Kreuz}
    zahl = random.randint(1, 10)  # Zahl von 1 bis 10 (du kannst 11-13 auch reinnehmen)
    symbol = random.randint(1, 4)
    color = RED if symbol < 3 else BLACK

    font = pygame.font.SysFont(None, int(card_height * 0.7))
    if zahl == 11:
        text_surface = font.render("J", True, color)
        text_rect = text_surface.get_rect(center=(x + card_width // 2, y + card_height // 2))
        surface.blit(text_surface, text_rect)
        for pos in mittelpunkte:
            symbole[symbol](*pos, 30)
    elif zahl == 12:
        text_surface = font.render("Q", True, color)
        text_rect = text_surface.get_rect(center=(x + card_width // 2, y + card_height // 2))
        surface.blit(text_surface, text_rect)
        for pos in mittelpunkte:
            symbole[symbol](*pos, 30)
    elif zahl == 13:
        text_surface = font.render("K", True, color)
        text_rect = text_surface.get_rect(center=(x + card_width // 2, y + card_height // 2))
        surface.blit(text_surface, text_rect)
        for pos in mittelpunkte:
            symbole[symbol](*pos, 30)
    else:
        for pos in mittelpunkte:
            symbole[symbol](*pos, 30)
        for pos in zahlen[zahl]:
            symbole[symbol](*pos, 40)
