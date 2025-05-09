import pygame

class Chip:
    def __init__(self, image_path, pos, radius=40):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.radius = radius
        self.image = pygame.transform.smoothscale(self.image, (radius * 2, radius * 2))
        self.pos = list(pos)  # [x, y]
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            dx = event.pos[0] - self.pos[0]
            dy = event.pos[1] - self.pos[1]
            if dx * dx + dy * dy <= self.radius * self.radius:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.pos = list(pygame.mouse.get_pos())  # <-- HIER!

    def draw(self, screen):
        screen.blit(self.image, (self.pos[0] - self.radius, self.pos[1] - self.radius))
