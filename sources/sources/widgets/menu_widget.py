import pygame

from sources.utils.colors import Colors
from sources.utils.utils import Utils
from sources.widgets.buttons.menu_button import MenuButton


class MenuWidget:
    """
    Classe qui permet l'affichage du Menu
    """

    def __init__(self, game):
        self.game = game

        # Liste des boutons présents dans le Menu
        self.menu_buttons = [
            MenuButton("Commencer", "start"),
            MenuButton("Tutoriel", "tutorial"),
            MenuButton("Charger une sauvegarde", "load")
        ]

    def draw(self):
        # Dessine le fond tamisé
        transparent_background = pygame.Surface(Utils.WINDOW_DIMENSION, pygame.SRCALPHA)
        transparent_background.fill((0, 0, 0, 128))
        self.game.screen.blit(transparent_background, (0, 0))

        # Titre du jeu
        font_title = pygame.font.Font(Utils.SCIENCE_FONT, 80)  # habillage du texte (police d'écriture, taille)
        title_text = font_title.render(Utils.APP_TITLE, True, Colors.BLANC)  # Contenue du texte
        title_rect = title_text.get_rect(center=(Utils.WIDTH_WINDOW_DIMENSION // 2, 100))  # Emplacement du texte
        self.game.screen.blit(title_text, title_rect)

        # Boutons
        button_y = 250  # Coord Y de chaque bouton
        for button in self.menu_buttons:
            button.draw(self.game.screen, button_y)
            button_y += 100  # Coord X de chaque bouton
