import pygame
import math

from sources.forms.forms import Forms
from sources.utils.colors import Colors


class Rectangular(Forms):
    """
    Polynôme pymunk de type rectangle
    """

    def __init__(self, identifier, key, body, size, texture_path, elasticity=0.8, friction=0.5):
        vertices = [(-size[0] / 2, size[1] / 2), (-size[0] / 2, -size[1] / 2), (size[0] / 2, -size[1] / 2), (size[0] / 2, size[1] / 2)]
        super().__init__(identifier, key, body, texture_path, elasticity, friction, vertices)

        self.texture = pygame.transform.scale(self.texture, size)
        self.size = size
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()


    def draw(self, surface):
        """
        Dessine la forme ainsi que la texture assignée
        """
        pos = self.body.position

        # Oriente l'image en fonction de l'angle de la forme
        rotated_texture = pygame.transform.rotate(self.texture, -math.degrees(self.body.angle))
        rect = rotated_texture.get_rect(center=pos)
        surface.blit(rotated_texture, rect)

        # Si l'image doit être mise en valeur, on l'entoure d'un carré rouge
        if self.highlighted:
            pygame.draw.rect(surface, Colors.ROUGE, rect, 2)