import pygame
import pygame.gfxdraw

from sources.utils.utils import Utils


class EnvironmentButton:
    """
    Permet d'afficher un bouton-environnement
    """

    def __init__(self, environment, text):
        self.environment = environment  # Environnement assigné au bouton

        self.initImage()

        self.text = text  # Nom de l'environnement
        self.font = pygame.font.Font(Utils.SCIENCE_FONT, 16)

    def initImage(self):
        """
        Initialise l'image assignée au bouton, et applique un contour
        :return:
        """
        self.image = pygame.image.load(self.environment.texture)
        self.image = pygame.transform.scale(self.image, (90, 60))
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Créer une surface pour le rectangle avec contour
        rounded_rect = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect, (255, 255, 255, 128), rounded_rect.get_rect(), border_radius=10)

        rounded_rect.blit(self.image, (0, 0))
        self.image = rounded_rect

    def draw(self, surface):
        """
        Dessine le bouton-environnement en question
        """
        surface.blit(self.image, self.rect)  # Dessine l'image liée au bouton
        pygame.draw.rect(surface, (255, 255, 255, 128), self.rect, 3)  # Ajouter un contour

        # Affiche le texte (= nom de l'environnement)
        text_rendered = self.font.render(self.text, False, (0, 0, 0))
        surface.blit(text_rendered, (self.rect.centerx - text_rendered.get_width() / 2, self.rect.bottom + 5))


    def isClicked(self, pos):
        """
        Renvoie True si le bouton est cliqué, sinon False
        """
        return self.rect.collidepoint(pos)

