import pygame

from sources.utils.colors import Colors
from sources.utils.texture import Texture
from sources.widgets.buttons.tool_button import ToolButton


class ToolsWidget:
    """
    Classe qui permet l'affichage de la "boite à outils"
    """

    def __init__(self, surface):
        self.surface = surface  # Surface sur laquelle sera dessiner le widget

        # Liste des boutons présents dans le Widget
        self.tools = [
            ToolButton("menu", Texture.ROOT_GENERAL + "home.png"),
            ToolButton("play", Texture.ROOT_GENERAL + "pause.png"),
            ToolButton("reset", Texture.ROOT_GENERAL + "reset.png"),
            ToolButton("save", Texture.ROOT_GENERAL + "save.png"),
            ToolButton("science", Texture.ROOT_GENERAL + "science.png"),
            ToolButton("link", Texture.ROOT_GENERAL + "link.png"),
        ]

        self.spacing = 20  # Espace entre chaque bouton
        self.bottom_padding = 10  # Espace entre le bas de l'écran et les boutons

    def draw(self):
        """
        Dessine la zone où se situent les différentes actions possibles sur le jeu
        """
        self.surface.fill(Colors.SABLE)

        background = pygame.image.load(Texture.BACKGROUND_ENVIRONMENT)  # On applique le fond d'écran
        self.surface.blit(background, (0, 0))

        # Application d'un contour sur la zone Tools
        pygame.draw.rect(self.surface, Colors.NOIR, self.surface.get_rect(), 2)

        x_offset = 10  # Espace entre la gauche de l'écran et le premier bouton
        y_position = self.surface.get_height() - self.bottom_padding - max(button.rect.height for button in self.tools)

        for i, tool in enumerate(self.tools):
            if i == 3:
                x_offset = 10
                y_position = 10
            tool.rect.topleft = (x_offset, y_position)
            tool.draw(self.surface)
            x_offset += tool.rect.width + self.spacing

    def checkClick(self, pos):
        """
        Si une action est touché, il la renvoie
        """
        for tool in self.tools:
            if tool.isClicked(pos):
                if tool.function == "play": # Si l'action en question est play, on modifie la texture du bouton
                    if tool.texture_path == Texture.ROOT_GENERAL + "play.png":
                        tool.texture_path = Texture.ROOT_GENERAL + "pause.png"
                        tool.initImage()
                    else:
                        tool.texture_path = Texture.ROOT_GENERAL + "play.png"
                        tool.initImage()
                return tool.function

        return None

    def updateEnvironment(self, environment):
        """
        Lorsque l'environnement est mis à jour, on modifie la texture du bouton Play en fonction de l'environnement
        """
        tool = self.tools[1]
        if environment.strong_freeze: # Si l'environnement est en pause, on met la texture sur Play.
            tool.texture_path = Texture.ROOT_GENERAL + "play.png"
            tool.initImage()
        else:
            tool.texture_path = Texture.ROOT_GENERAL + "pause.png"
            tool.initImage()
