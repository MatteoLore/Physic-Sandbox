import pygame

from sources.utils.colors import Colors
from sources.utils.utils import Utils


class FormButton:
    """
    Permet l'affichage d'un bouton-figure
    """

    def __init__(self, form, text, texture_path):
        self.form = form  # Figure associée au bouton
        self.texture_path = texture_path  # Texture associée au bouton

        self.initImage()
        self.resizeImage()

        self.text = text  # Nom de la figure
        self.font = pygame.font.Font(Utils.SCIENCE_FONT, 13)

    def initImage(self):
        """
        Initialise l'image assignée au bouton-figure
        """
        self.image = pygame.image.load(self.texture_path)
        self.rect = self.image.get_rect(topleft=(0, 0))

    def resizeImage(self):
        """
        Redimensionne l'image pour qu'elle soit adapté à la taille du bouton
        """
        max_size = 75
        min_size = 10

        # Redimensionne l'image tout en maintenant les proportions
        ratio = min(max_size / self.rect.width, max_size / self.rect.height)
        new_width = int(self.rect.width * ratio)
        new_height = int(self.rect.height * ratio)

        # Vérifie que la nouvelle taille est dans la plage autorisée
        if new_width < min_size and self.rect.width > min_size:
            new_width = min_size
            new_height = int(self.rect.height * (min_size / self.rect.width))
        elif new_height < min_size and self.rect.height > min_size:
            new_height = min_size
            new_width = int(self.rect.width * (min_size / self.rect.height))

        # Redimensionne l'image
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface):
        """
        Dessine le bouton-figure
        """
        surface.blit(self.image, self.rect)  # Dessine l'image liée au bouton

        # Affiche le texte (= nom du bouton)
        lines = self.wrap_text(self.font, self.text, self.rect.width - 10)
        y_offset = self.rect.bottom + 5  # Espacement entre le bas du bouton et le texte
        for line in lines:
            text_rendered = self.font.render(line, True, Colors.NOIR)
            surface.blit(text_rendered, (self.rect.centerx - text_rendered.get_width() / 2, y_offset))
            y_offset += text_rendered.get_height()

    def isClicked(self, pos):
        """
        Renvoie True si le bouton est cliqué, sinon False
        """
        return self.rect.collidepoint(pos)

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
