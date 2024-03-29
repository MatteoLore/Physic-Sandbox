import pygame

from sources.environments.mars_environment import MarsEnvironment
from sources.environments.reversed_environment import ReversedEnvironment
from sources.environments.water_environment import WaterEnvironment
from sources.utils.colors import Colors
from sources.utils.texture import Texture
from sources.widgets.buttons.environment_button import EnvironmentButton


class EnvironmentsWidget:
    """
    Classe qui permet l'affichage de la zone des environnements
    """

    def __init__(self, surface, default_environment):
        self.surface = surface

        # Liste des boutons présents dans le Widget
        self.environments = [
            EnvironmentButton(default_environment, "Laboratoire"),
            EnvironmentButton(MarsEnvironment(), "Mars"),
            EnvironmentButton(WaterEnvironment(), "Aquarium"),
            EnvironmentButton(ReversedEnvironment(), "Monde Inverse"),
        ]

        # Environnement chargé par l'utilisateur, indépendant des environnements par défaut
        self.load_environments = []

        self.spacing = 110  # Espace entre chaque bouton
        self.bottom_padding = 20  # Espace entre le bas de l'écran et les boutons

        self.environments_view = []

        self.key_start = 0  # Indice de départ de la liste des figures affichées
        self.setViewList()

    def addLoadEnvironment(self, environment, name):
        """
        Ajoute à la liste un nouvel environnement chargé par l'utilisateur
        """

        self.load_environments.append(EnvironmentButton(environment, name))

        self.key_start = len(self.environments+self.load_environments)-3  # Met à jour l'indice d'affichage pour faire apparaitre le nouvel environnement
        self.setViewList()

    def draw(self):
        """
        Dessine la zone de choix des différents environnements/mondes disponibles
        """
        self.surface.fill(Colors.BEIGE)  # On efface tout

        background = pygame.image.load(Texture.BACKGROUND_ENVIRONMENT)  # On applique le fond d'écran
        self.surface.blit(background, (0, 0))

        x_offset = 40  # Espace entre la gauche de l'écran et le premier bouton
        y_position = self.surface.get_height() - self.bottom_padding - max(environment.rect.height for environment in self.environments)

        # On dessine chaque bouton-environnement
        for environment in self.environments_view:
            if isinstance(environment, ScrollButton):
                environment.rect.topleft = (x_offset, -5)
            else:
                environment.rect.topleft = (x_offset, y_position)
            environment.draw(self.surface)
            x_offset += environment.rect.width + self.spacing

    def checkClick(self, pos):
        """
        Si un environnement est touché, il le renvoie
        """
        for environment in self.environments_view:
            if environment.isClicked(pos):
                if isinstance(environment, ScrollButton):  # On augmente l'indice de départ de la liste d'affichage
                    self.key_start += 1
                    self.setViewList()
                else:
                    return environment
        return None

    def setViewList(self):
        """
        Définit la liste des environnements qui seront affichés
        """
        environments = self.environments+self.load_environments

        if len(environments) < 3:
            self.environments_view = environments
        else:  # Le nombres d'environnements est trop important, on limite à 3 environnements affichés (avec un système de défilement)
            if self.key_start + 2 == len(environments):
                self.key_start = -2
            elif self.key_start == -(len(environments)):
                self.key_start = 0
            x = self.key_start

            button = [ScrollButton(), environments[x], environments[x + 1], environments[x + 2]]
            self.environments_view = button


class ScrollButton:
    """
    Bouton permettant de se déplacer dans le widget environnement.
    """

    def __init__(self):
        self.image = pygame.image.load(Texture.ROOT_GENERAL +"scroll_button.png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

