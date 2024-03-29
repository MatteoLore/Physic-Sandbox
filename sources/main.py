import pygame
from sources.environments.main_environment import MainEnvironment
from sources.listeners.listeners_manager import ListenersManager
from sources.utils.colors import Colors
from sources.utils.utils import Utils
from sources.widgets.environments_widget import EnvironmentsWidget
from sources.widgets.menu_widget import MenuWidget
from sources.widgets.tools_widget import ToolsWidget
from sources.widgets.forms_widget import FormsWidget
from sources.widgets.tutorial_widget import TutorialWidget


class Game:
    """
    Classe principale du programme, elle permet l'articulation de l'ensemble des classes.
    """

    def __init__(self):
        self.initGame()
        self.initWidgets()
        self.initListener()

        self.menu_active = True
        self.tutorial_active = False

        self.link_active = False

    def initGame(self):
        """
        Initialise le jeu, définit l'environnement par défaut, la taille de la fenêtre principale et de la zone de jeu
        :return:
        """
        self.screen = pygame.display.set_mode(Utils.WINDOW_DIMENSION, pygame.SRCALPHA)  # Taille de la fenêtre de jeu
        self.sandbox = pygame.Surface(Utils.SANDBOX_DIMENSION)  # Zone de jeu physique
        self.active_environment = MainEnvironment()  # Environnement par défaut

        pygame.display.set_caption(Utils.APP_TITLE)  # Nom de la fenêtre
        pygame.display.set_icon(pygame.image.load("resources/general/logo.png").convert())  # Icone de l'application

        self.screen.fill(Colors.BLANC)  # background -> blanc
        self.sandbox.fill(Colors.GRIS)  # background -> gris

    def initWidgets(self):
        """
        Initialise les différentes zones d'interactions de la fenêtre principale
        """
        self.environment_surface = pygame.Surface((850, 100))  # Zone où se situent les différents environnements
        self.forms_surface = pygame.Surface((100, 600))  # Zone où se situent les différentes figures
        self.tools_surface = pygame.Surface((150, 100))  # Zone où se situent les interactions principales avec le jeu.

        # Définitions de leurs couleurs de fonds
        self.forms_surface.fill(Colors.BEIGE)
        self.environment_surface.fill(Colors.BEIGE)
        self.tools_surface.fill(Colors.BEIGE)

        # Définitions des Widgets / zones d'interactions de la fenêtre
        self.forms_widget = FormsWidget(self.forms_surface, self.active_environment)
        self.environments_widget = EnvironmentsWidget(self.environment_surface, self.active_environment)
        self.tools_widget = ToolsWidget(self.tools_surface)

        self.menu_widget = MenuWidget(self)
        self.tutorial_widget = TutorialWidget(self)

    def initListener(self):
        """
        Initialise le centre d'écoute des événements du jeu
        """
        self.listener = ListenersManager(self)

    def drawWidgets(self):
        """
        Dessine les différentes zones d'interactions (=widgets) de la fenêtre
        """
        self.environments_widget.draw()
        self.forms_widget.draw()
        self.tools_widget.draw()

    def updateEnvironment(self, button):
        """
        Met à jour l'environnement de jeu, ansi que les figures liées à ce dernier
        """
        self.link_active = False
        self.active_environment = button.environment
        self.forms_widget.setEnvironment(self.active_environment)

        self.listener.updateEnvironment()
        self.tools_widget.updateEnvironment(self.active_environment)

    def run(self):
        """
        Boucle principale de l'application, elle permet de faire fonctionner chaque interface et zone de jeu.
        """
        running = True
        while running:
            # On transmet chaque événement au ListenerManager qui les prend en charges et agit en consèquence
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'évenement est QUIT (= la croix de la fênetre), on met fin à la boucle.
                    running = False
                elif self.menu_active:
                    self.listener.dispatchMenuEvents(event)
                else:
                    self.listener.dispatchEvents(event)

            # On met à jour l'environnement et la zone de jeu
            self.active_environment.update()
            self.active_environment.draw(self.sandbox)
            self.drawWidgets()

            # On affiche les zones de jeu actualisé de notre app
            self.screen.blit(self.sandbox, (0, 0))
            self.screen.blit(self.environment_surface, (0, 600))
            self.screen.blit(self.forms_surface, (900, 0))
            self.screen.blit(self.tools_surface, (850, 600))

            # Si le menu est activé (= l'utilisateur se situe dans le menu), alors on affiche le menu
            if self.menu_active:
                self.menu_widget.draw()

            # Si le tutoriel est activé (=l'utilisateur a lancé le tutoriel), alors on affiche le tutoriel
            elif self.tutorial_active:
                self.tutorial_widget.draw()

            # On affiche une image qui suit la souris si demandé
            if self.listener.mouse_tracker is not None:
                image = pygame.image.load(self.listener.mouse_tracker)
                if self.listener.link:
                    image = pygame.transform.scale(image, (28, 28))
                image_rect = image.get_rect()
                image_rect.center = pygame.mouse.get_pos()
                self.screen.blit(image, image_rect)

            clock = pygame.time.Clock()
            clock.tick(60)  # Fréquence de rafraichissement
            pygame.display.flip()

        pygame.quit()


"""
Lancement du programme en initialisant la class Game et le module Pygame 
"""
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
