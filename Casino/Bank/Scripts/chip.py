import pygame

class Chips:
    def __init__(self, image_path, pos, screen_size, radius_factor=0.035):

        self.image_path = image_path
        self.pos = list(pos)  # [x, y]
        self.radius_factor = radius_factor
        self.dragging = False
        self.update_radius(screen_size)

    def update_radius(self, screen_size):

        min_dim = min(screen_size)
        self.radius = int(min_dim * self.radius_factor)
        raw_image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(raw_image, (self.radius * 2, self.radius * 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            dx = event.pos[0] - self.pos[0]
            dy = event.pos[1] - self.pos[1]
            if dx * dx + dy * dy <= self.radius * self.radius:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.pos = list(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.blit(self.image, (self.pos[0] - self.radius, self.pos[1] - self.radius))

    def collides_with_rect(self, rect: pygame.Rect) -> bool:
        # Finde den nächsten Punkt auf dem Rechteck relativ zum Kreiszentrum
        closest_x = max(rect.left, min(self.pos[0], rect.right))
        closest_y = max(rect.top, min(self.pos[1], rect.bottom))

        # Berechne die Distanz vom Kreiszentrum zum nächstgelegenen Punkt
        dx = self.pos[0] - closest_x
        dy = self.pos[1] - closest_y

        # Prüfe, ob diese Distanz kleiner oder gleich dem Radius ist
        return dx * dx + dy * dy <= self.radius * self.radius
