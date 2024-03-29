import pygame

from sources.utils.colors import Colors
from sources.utils.texture import Texture


class TutorialWidget:
    """
    Classe qui permet l'affichage du tutoriel.
    """

    def __init__(self, game):
        self.game = game

        self.position = (50, 50)
        self.size = ()

        self.character_image = pygame.image.load(Texture.TUTORIAL)  # Personnage à afficher

        self.text = ""  # Texte à afficher
        self.mask_area = []  # Zones à masquer


    def draw(self):
        self.character_image = pygame.transform.scale(self.character_image, (self.size))  # (150, 200))
        self.character_rect = self.character_image.get_rect(topleft=self.position)
        font = pygame.font.Font(None, 40)
        text_lines = self.wrap_text(font, self.text, 700)  # Diviser le texte en lignes
        text_rect = self.character_rect.copy()
        text_rect.left = self.character_rect.right + 20  # Positionnez le texte à droite du personnage  # Positionne le texte à droite du personnage

        # Masque les zones souhaitées
        for area in self.mask_area:
            transparent_background = pygame.Surface((area[0].get_width(), area[0].get_height()), pygame.SRCALPHA)
            transparent_background.fill((0, 0, 0, 200)) # Couleur Opaque (changer derniere valeur pour la transparence)
            self.game.screen.blit(transparent_background, area[1])

        # Dessine le personnage
        self.game.screen.blit(self.character_image, self.character_rect)

        # Dessine chaque ligne de texte
        for line in text_lines:
            text_surface = font.render(line, True, Colors.BLANC)
            self.game.screen.blit(text_surface, text_rect.topleft)
            text_rect.top += text_surface.get_height()


    def wrap_text(self, font, text, max_width):
        """Divise le texte en lignes qui tiennent dans la largeur maximale spécifiée."""
        lines = []
        for line in text.split('\n'):  # Sépare le texte à chaque occurrence de '\n'
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + ' ' + word if current_line else word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
        return lines
