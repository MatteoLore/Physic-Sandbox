import math

import pymunk
import pymunk.autogeometry as autogeometry
import pygame
from pymunk import Vec2d

from sources.forms.forms import Forms
from sources.utils.colors import Colors


class AutogeometryShape(Forms):
    """
    Polynôme pymunk généré à partir de n'importe quelle image
    """

    def __init__(self, identifier, key, body, texture_path, elasticity=0.8, friction=0.5):
        self.texture = pygame.image.load(texture_path)
        vertices = self.generateVertices()
        super().__init__(identifier, key, body, texture_path, elasticity, friction, vertices)


    def draw(self, surface):
        """
        Dessine la forme ainsi que la texture assignée
        """
        pos = self.body.position

        # Calcul du centre de la forme avec rotation
        center_offset = Vec2d(self.width / 2, self.height / 2)
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

    def generateVertices(self):
        """
        Génére les sommets de la figure à partir de la texture assignés
        Utilise pymunk.autogeometry module
        """
        image_bb = pymunk.BB(0, 0, self.texture.get_width(), self.texture.get_height())

        # On repère les lignes de l'image
        line_set = pymunk.autogeometry.march_hard(
            image_bb, self.texture.get_width(), self.texture.get_height(), 99, self.getPixelColor
        )

        vertices = []
        # Pour chaque ligne, on récupère tous les points
        for line in line_set:
            # Simplification des courbes dans la géométrie
            line = pymunk.autogeometry.simplify_curves(line, 0.7)
            for point in line:
                vertices.append((point.x, point.y))

        return vertices

    def getPixelColor(self, point):
        """
        Renvoie la couleur du pixel (=point)
        """
        try:
            p = pymunk.pygame_util.to_pygame(point, self.texture)
            color = self.texture.get_at(p)
            return color.a
        except:
            return 0

