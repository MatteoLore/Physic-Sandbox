import pygame

from sources.listeners.environment_surface_listener import EnvironmentSurfaceListener
from sources.listeners.forms_surface_listener import FormsSurfaceListener
from sources.listeners.menu_listener import MenuListener
from sources.listeners.sandbox_listener import SandboxListener
from sources.listeners.tools_surface_listener import ToolsSurfaceListener
from sources.listeners.tutorial_listener import TutorialListener


class ListenersManager:
    """
    Centre d'écoute des événements, les dispatch aux centres d'écoutes inférieurs
    """

    def __init__(self, game):
        self.game = game

        self.initListeners()

        self.initRect()

        self.selected_form = None
        self.moved_form = None
        self.link = False
        self.link_form = None

        self.mouse_tracker = None

    def updateEnvironment(self):
        """
        Réinitialise les propriétés de la classe lorsque l'environnement est changé
        """
        self.selected_form = None
        self.moved_form = None
        self.link = False
        self.link_form = None
        self.mouse_tracker = None

    def initListeners(self):
        """
        Initialisation des différents centres d'écoutes (en fonction de leur zone)
        """
        self.environment = EnvironmentSurfaceListener(self)
        self.forms = FormsSurfaceListener(self)
        self.tools = ToolsSurfaceListener(self)
        self.sandbox = SandboxListener(self)

        self.menu = MenuListener(self)
        self.tutorial = TutorialListener(self)

    def initRect(self):
        """
        Initialisation des différentes positions des zones présentes dans la fenêtre de jeu
        """
        self.environment_rect = self.game.environment_surface.get_rect(topleft=(0, 600))
        self.forms_rect = self.game.forms_surface.get_rect(topleft=(900, 0))
        self.tools_rect = self.game.tools_surface.get_rect(topleft=(850, 600))
        self.sandbox_rect = self.game.sandbox.get_rect(topleft=(0, 0))



    def dispatchEvents(self, event):
        """
        Dispatch les événements à leur centre d'écoute en fonction de leurs zones et du type d'évènements
        """
        # Click gauche enclenché
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.environment_rect.collidepoint(event.pos):
                self.environment.changeEnvironment(pos)
                self.dispatchTutorial("change environnement")

            elif self.forms_rect.collidepoint(event.pos):
                self.forms.setSelectedForm(pos)

            elif self.tools_rect.collidepoint(event.pos):
                self.tools.executeToolFunction(pos)

            elif self.sandbox_rect.collidepoint(event.pos):
                self.sandbox.leftDownClick(pos)
                self.dispatchTutorial("tout")

        # Click gauche relaché
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            if self.sandbox_rect.collidepoint(event.pos):
                self.sandbox.leftUpClick()

        # Mouvement de la souris
        elif event.type == pygame.MOUSEMOTION:

            if self.sandbox_rect.collidepoint(event.pos):
                self.sandbox.motionCursor(pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.sandbox_rect.collidepoint(event.pos):
                self.sandbox.rightDownClick(pos)
                self.dispatchTutorial("proprietes forme")

    def dispatchMenuEvents(self, event):
        """
        Lorsque le menu est activé, le dispatch d'événements est différents, il n'existe qu'une seule zone
        """
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.menu.leftDownClick(pos, self.game.menu_widget.menu_buttons)


    def dispatchTutorial(self, event):
        """
        Si le tutoriel est activé, on renvoie le type d'événement au tutoriel listener.
        """
        if self.game.tutorial_active:
            self.tutorial.eventTutorial(event)





