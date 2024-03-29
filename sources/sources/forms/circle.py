import math

import pygame
import pymunk

from sources.utils.colors import Colors


class Circle(pymunk.Circle):
    """
    Cercle pymunk
    """

    def __init__(self, id, key, body, radius, texture_path, elasticity=0.8, friction=0.5):
        body.moment = pymunk.moment_for_circle(body.mass, 0, radius)
        super().__init__(body, radius)

        # Propriétés utiles à l'environnement
        self.id = id
        self.key = key
        self.type = 0
        self.highlighted = False

        # Propriétés textures
        self.texture_path = texture_path
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (int(radius * 2), int(radius * 2)))

        # Propriétés physiques
        self.elasticity = elasticity
        self.friction = friction
        self.mass = body.mass

        self.last_force = (0, 0)
        self.last_velocity = (0, 0)
        self.last_rotation = 0

    def draw(self, surface):
        """
        Dessine la figure en question
        """
        position = self.body.position

        # Oriente l'image en fonction de l'angle de la forme
        texture = pygame.transform.rotate(self.texture, math.degrees(-self.body.angle))
        draw_position = (int(position.x), int(position.y))
        draw_rect = texture.get_rect(center=draw_position)
        surface.blit(texture, draw_rect)

        # Si l'image doit être mise en valeur, on l'entoure d'un carré rouge
        if self.highlighted:
            pygame.draw.rect(surface, Colors.ROUGE, draw_rect, 2)

    def updateType(self, type_value):
        """
        Met à jour le status de la figure, statique ou non statique
        """
        if type_value == 1 and self.type == 0: # Si la valeur est statique alors on accroche la forme à un objet statique pour la rendre statique

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

    def isClicked(self, pos):
        """
        Renvoie True si le bouton est cliqué, sinon False
        """
        position = self.body.position
        radius = self.radius

        distance = math.sqrt((pos[0] - position.x) ** 2 + (pos[1] - position.y) ** 2)
        return distance <= radius

    def printInfo(self, surface):
        """
        Affiche les informations de la figure (position et forces)
        """
        font = pygame.font.Font(None, 18)
        position = self.body.position

        if self.body.velocity == (0, 0): # Si la forme est immobilisé, on récupére les dernières forces enregistrées avant l'immobilisation
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

        text_position_x = position.x - text_vertical_force.get_width() // 2
        text_position_y = position.y - self.radius - 40

        # On affiche l'ensemble, avec des positions calculé
        surface.blit(text_vertical_force, (text_position_x, text_position_y))
        surface.blit(text_horizontal_force, (text_position_x, text_position_y + text_vertical_force.get_height()))
        surface.blit(text_position, (text_position_x, text_position_y + text_vertical_force.get_height() + text_horizontal_force.get_height()))

    def getCenter(self):
        """
        Renvoie le centre de la figure
        """
        return self.body.position
