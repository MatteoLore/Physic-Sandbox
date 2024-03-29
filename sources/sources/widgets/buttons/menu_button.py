import pygame

from sources.utils.colors import Colors
from sources.utils.texture import Texture
from sources.utils.utils import Utils


class MenuButton:
    """
    Permet d'afficher un bouton du menu
    """

    def __init__(self, text, function):
        self.text = text  # Texte assigné au bouton
        self.function = function  # Fonction assignée au bouton

        self.rect = pygame.Rect(0, 0, 380, 60)  # Dimension du rectangle

    def draw(self, screen, y):
        """
        Dessine le bouton avec un fond
        """
        font = pygame.font.Font(Utils.SCIENCE_FONT, 26)

        # Charge l'image de fond
        background_image = pygame.image.load(Texture.BACKGROUND_ENVIRONMENT)

        # Redimensionne l'image pour s'adapter à la taille du bouton
        background_image = pygame.transform.scale(background_image, (self.rect.width, self.rect.height))

        # Dessine l'image de fond
        screen.blit(background_image, self.rect)

        button_text = font.render(self.text, True, Colors.NOIR)

        self.rect.center = (screen.get_width() // 2, y)


        pygame.draw.rect(screen, Colors.NOIR, self.rect, 3)
        # Dessine le texte au centre du rectangle
        text_rect = button_text.get_rect(center=self.rect.center)
        screen.blit(button_text, text_rect)


    def getFunction(self):
        """
        Renvoie la fonction du bouton
        """
        return self.function

    def isClicked(self, pos):
        """
        Renvoie True si le bouton est cliqué, sinon False
        """
        return self.rect.collidepoint(pos)

