import pygame
import pymunk
from pymunk import Poly

from sources.utils.colors import Colors


class Forms(Poly):
    """
    Polynôme pymunk, utilisable dans n'importe quel environnement
    """

    def __init__(self, identifier, key, body, texture_path, elasticity, friction, vertices):
        body.moment = pymunk.moment_for_poly(body.mass, vertices)
        super().__init__(body, vertices)

        # Propriétés utiles à l'environnement
        self.id = identifier
        self.key = key
        self.type = 0
        self.highlighted = False

        # Propriétés textures
        self.texture_path = texture_path
        self.texture = pygame.image.load(texture_path)
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()

        # Propriétés physiques
        self.elasticity = elasticity
        self.friction = friction
        self.mass = body.mass

        self.last_force = (0, 0)
        self.last_velocity = (0, 0)
        self.last_rotation = 0


    def isClicked(self, pos):
        """
        Renvoie True si le point pos est à l'intérieur du polygone, sinon False
        """
        vertices = self.get_vertices()
        x = pos[0] - self.body.position.x
        y = pos[1] - self.body.position.y
        n = len(vertices)
        inside = False

        # Position du premier sommet
        p1x, p1y = vertices[0]
        for i in range(n + 1):
            # Position du deuxième sommet
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):  # au-dessus du segment
                if y <= max(p1y, p2y):  # en dessous du segment
                    if x <= max(p1x, p2x):  # gauche du segment
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def updateType(self, type_value):
        """
        Met à jour le status de la figure, statique ou non statique
        """
        if type_value == 1 and self.type == 0:  # Si la valeur est statique alors on accroche la forme à un objet statique pour la rendre statique

            static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            static_body.position = self.body.position

            pin_joint = pymunk.PinJoint(self.body, static_body, (0, 0), (0, 0))

            self.body.space.add(pin_joint)

            self.type = 1
        elif type_value == 0 and self.type == 1:  # Sinon on supprime toute attache à un corp statique
            for joint in self.body.constraints:
                if joint in self.space.constraints and isinstance(joint, pymunk.PinJoint):
                    self.space.remove(joint)
            self.type = 0

    def removeJoints(self):
        """
        Supprime tous les liens qui relient la figure à une autre
        """
        for joint in self.body.constraints:
            if joint in self.space.constraints and not isinstance(joint, pymunk.PinJoint):
                self.space.remove(joint)

    def getCenter(self):
        """
        Renvoie le centre de la figure
        """
        centroid_x = 0
        centroid_y = 0
        taille = 0
        for x, y in self.get_vertices():  # Calcul du centroid
            centroid_x += x
            centroid_y += y
            taille += 1

        return centroid_x/taille, centroid_y/taille

    def printInfo(self, surface):
        """
        Affiche les informations de la figure (position et forces)
        """
        font = pygame.font.Font(None, 18)
        position = self.body.position + self.getCenter()

        if self.body.velocity == (0, 0):  # Si la forme est immobilisé, on récupére les dernières forces enregistrées avant l'immobilisation
            forces = self.last_velocity
        else:
            forces = self.body.velocity

        # On définit les textes à afficher
        vertical_force_str = f"Force Verticale: {forces[1]:.2f}"
        horizontal_force_str = f"Force Horizontale: {forces[0]:.2f}"
        position_str = f"Position: ({position.x:.2f}, {position.y:.2f})"

        # On habille le contenu
        text_vertical_force = font.render(vertical_force_str, True, Colors.NOIR)
        text_horizontal_force = font.render(horizontal_force_str, True, Colors.NOIR)
        text_position = font.render(position_str, True, Colors.NOIR)

        rect = self.texture.get_rect()
        text_position_x = position[0] - rect.width // 2
        text_position_y = position[1] - (rect.height + 15)

        # On affiche l'ensemble, avec des positions calculé
        surface.blit(text_vertical_force, (text_position_x, text_position_y))
        surface.blit(text_horizontal_force, (text_position_x, text_position_y + text_vertical_force.get_height()))
        surface.blit(text_position, (
        text_position_x, text_position_y + text_vertical_force.get_height() + text_horizontal_force.get_height()))
