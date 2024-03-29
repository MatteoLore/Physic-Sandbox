import pygame

from sources.utils.colors import Colors


class ToolButton:
    """
    Permet l'affichage d'un bouton-outil
    """

    def __init__(self, function, texture_path):
        self.function = function  # fonction assignée au bouton
        self.texture_path = texture_path  # texture assignée au bouton

        self.initImage()

    def initImage(self):
        """
        Initialise l'image assignée au bouton
        """
        self.image = pygame.image.load(self.texture_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(0, 0))


    def draw(self, surface):
        """
        Dessine le bouton
        """
        # Dessine l'image liée au bouton
        surface.blit(self.image, self.rect)


    def isClicked(self, pos):
        """
        Renvoie True si le bouton est cliqué, sinon False
        """
        return self.rect.collidepoint(pos)
