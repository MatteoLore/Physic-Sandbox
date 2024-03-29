import math

import pygame
from pymunk.vec2d import Vec2d

from sources.forms.forms import Forms
from sources.utils.colors import Colors


class Triangle(Forms):
    """
    Polynôme pymunk de type triangle rectangle
    """

    def __init__(self, identifier, key, body, size, texture_path, elasticity=0.8, friction=0.5):
        vertices = [(0, 0), (0, -size[1]), (size[0], 0)]
        super().__init__(identifier, key, body, texture_path, elasticity, friction, vertices)

        self.texture = pygame.transform.scale(self.texture, size)
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.size = size


    def draw(self, surface):
        """
        Dessine la forme ainsi que la texture assignée
        """
        pos = self.body.position

        # Calcul du centre de la forme avec rotation
        center_offset = Vec2d(self.width / 2, -self.height / 2)
        rotated_offset = center_offset.rotated(self.body.angle)
        center = pos + rotated_offset

        # Oriente l'image en fonction de l'angle de la forme
        rotated_texture = pygame.transform.rotate(self.texture, -math.degrees(
            self.body.angle))
        rect = rotated_texture.get_rect(center=center)
        surface.blit(rotated_texture, rect)

        # Si l'image doit être mise en valeur, on l'entoure d'un carré rouge
        if self.highlighted:
            pygame.draw.rect(surface, Colors.ROUGE, rect, 2)
