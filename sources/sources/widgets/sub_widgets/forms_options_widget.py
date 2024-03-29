import pygame
from pygame.locals import K_BACKSPACE, K_ESCAPE, K_RETURN

from sources.utils.colors import Colors
from sources.utils.texture import Texture
from sources.widgets.sub_widgets.properties_widget import PropertiesWidget


class FormsOptionsWidget:
    """
    Permet l'affichage de la boîte de dialogue des différentes actions possibles sur une figure
    """

    def __init__(self, figure, pos):
        self.figure = figure

        self.pos = pos  # Position de la boîte de dialogue

        # Taille de la boîte de dialogue
        self.width = 150
        self.height = 80

        self.options = ["Supprimer", "Propriétés", "Supprimer les liens"]  # Actions possibles

    def draw(self, surface):
        """
        Affiche la boîte de dialogue
        """
        # Dessine la boîte de dialogue (taille et fond)
        background = pygame.image.load(Texture.BACKGROUND_ENVIRONMENT).convert()
        background = pygame.transform.scale(background, (self.width, self.height))
        surface.blit(background, (self.pos[0], self.pos[1], self.width, self.height))

        pygame.draw.rect(surface, Colors.NOIR, (self.pos[0], self.pos[1], self.width, self.height), 2)

        # Dessiner le texte des options
        font = pygame.font.Font(None, 20)
        for i, option in enumerate(self.options):
            text_rendered = font.render(option, True, Colors.NOIR)
            text_rect = text_rendered.get_rect(
                center=(self.pos[0] + self.width // 2, self.pos[1] + (i + 0.5) * self.height / len(self.options)))
            surface.blit(text_rendered, text_rect)

    def isClicked(self, pos):
        """
        Si un bouton est touché, l'indice de ce dernier est renvoyée.
        """
        # On vérifie si la pos se situe dans la zone du bouton
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                self.pos[0],
                self.pos[1] + i * self.height // len(self.options),
                self.width,
                self.height // len(self.options)
            )
            if option_rect.collidepoint(pos):
                return i + 1
        return None

    def isPointInRect(self, point, rect):
        """
        Vérifie si le point se situe dans la zone donnée
        """
        return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]

    @staticmethod
    def showContextMenu(context_menu, manager):
        """
        Boucle permettant de gérer l'affichage et les événements en lien avec la boîte de dialogue.
        """
        properties_menu = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if properties_menu:
                            running = properties_menu.handle_events(event)
                        elif context_menu.isClicked(pos) == 1:  # Supprime la forme
                            manager.game.active_environment.deleteShape(context_menu.figure)
                            running = False
                        elif context_menu.isClicked(pos) == 2:  # Ouvre les propriétés
                            properties_menu = PropertiesWidget(context_menu.figure)
                        elif context_menu.isClicked(pos) == 3:  # Supprime les liens de la figure
                            context_menu.figure.removeJoints()
                            running = False
                        else:
                            running = False

            context_menu.draw(manager.game.screen)
            if properties_menu:  # Si les propriétés sont active, ont affiche l'interface en question
                properties_menu.draw(manager.game.screen)
            pygame.display.flip()

        pygame.display.update()
