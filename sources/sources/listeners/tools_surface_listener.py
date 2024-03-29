from sources.environments.environment import Environment
from sources.environments.main_environment import MainEnvironment
from sources.environments.mars_environment import MarsEnvironment
from sources.environments.reversed_environment import ReversedEnvironment
from sources.environments.water_environment import WaterEnvironment
from sources.utils.database import Database


class ToolsSurfaceListener:
    """
    Dirige les événements liés à la boîte à outils
    """

    def __init__(self, manager):
        self.manager = manager  # Centre d'écoute général

    def executeToolFunction(self, pos):
        """
        Execute la fonction du bouton-outil sélectionné
        """
        active_environment = self.manager.game.active_environment
        clicked_button = self.manager.game.tools_widget.checkClick((pos[0] - 850, pos[1] - 600))
        if clicked_button == "menu":  # Active le menu
            if not self.manager.game.tutorial_active:
                self.manager.game.menu_active = True
            self.manager.dispatchTutorial("manipuler outils")
        elif clicked_button == "reset":  # Réinitialise l'environnement
            active_environment.reset()
            self.manager.dispatchTutorial("manipuler outils")
        elif clicked_button == "play":
            self.play()
            self.manager.dispatchTutorial("manipuler outils")
        elif clicked_button == "science":  # Active le mode science
            active_environment.modeScience()
            self.manager.dispatchTutorial("manipuler microscope")
        elif clicked_button == "save":
            self.save()
            self.manager.dispatchTutorial("manipuler outils")
        elif clicked_button == "link":
            self.link()
            self.manager.dispatchTutorial("manipuler lien")

    def play(self):
        """
        Met en pause / en jeu l'environnement actuel
        """
        active_environment = self.manager.game.active_environment
        if active_environment.strong_freeze:
            active_environment.play()
        else:
            active_environment.stop()

    def link(self):
        """
        Active/désactive l'outil de lien entre figure
        """
        if self.manager.link:
            self.manager.link = False
            self.manager.game.link_active = False
            self.manager.mouse_tracker = None
        else:
            self.manager.link = True
            self.manager.game.link_active = True
            self.manager.mouse_tracker = "resources/general/link.png"

    def save(self):
        """
        Enregistre l'environnement actuel dans une base de données
        """
        if not self.manager.game.tutorial_active:
            active_environment = self.manager.game.active_environment
            save = active_environment.save()
            if isinstance(save, Database):
                data = Database.loadEnvironment(save.file)
                if data is not None:
                    environment = None
                    if data[0]["id"] == 1:
                        environment = MainEnvironment()
                    elif data[0]["id"] == 2:
                        environment = MarsEnvironment()
                    elif data[0]["id"] == 3:
                        environment = WaterEnvironment()
                    elif data[0]["id"] == 4:
                        environment = ReversedEnvironment()
        
                    if isinstance(environment, Environment):
                        environment.database = data[3]
                        environment.load(data[1], data[2])
        
                        self.manager.game.environments_widget.addLoadEnvironment(environment, data[0]["name"])
                        active_environment.reset()
                        active_environment.database = None
        
                        self.manager.game.active_environment = environment

