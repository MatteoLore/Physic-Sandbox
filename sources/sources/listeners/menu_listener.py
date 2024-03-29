from sources.environments.main_environment import MainEnvironment
from sources.environments.mars_environment import MarsEnvironment
from sources.environments.reversed_environment import ReversedEnvironment
from sources.environments.water_environment import WaterEnvironment
from sources.utils.database import Database


class MenuListener:
    """
    Dirige les événements liés au menu
    """

    def __init__(self, manager):
        self.manager = manager  # Centre d'écoute général

    def leftDownClick(self, pos, menu_buttons):
        """
        Execute la fonction du bouton-menu sélectionné.
        """
        for button in menu_buttons:
            if button.isClicked(pos):
                function = button.getFunction()
                if function == "start":
                    self.launchGame()
                elif function == "tutorial":
                    self.launchTutorial()
                elif function == "load":
                    self.loadEnvironment()

    def launchGame(self):
        """
        Lance le jeu et quitte le menu
        """
        game = self.manager.game
        game.menu_active = False

    def launchTutorial(self):
        """
        Lance le tutoriel et quitte le tutoriel
        """
        game = self.manager.game
        game.tutorial_active = True
        game.menu_active = False

    def loadEnvironment(self):
        """
        Charge un monde à partir d'un fichier que l'utilisateur est amené à sélectionner, puis lance le jeu
        """
        game = self.manager.game
        data = Database.loadEnvironment()
        if data is not None:  # On repère le type d'environnement à partir de l'identifiant
            if data[0]["id"] == 1:
                environment = MainEnvironment()
            elif data[0]["id"] == 2:
                environment = MarsEnvironment()
            elif data[0]["id"] == 3:
                environment = WaterEnvironment()
            elif data[0]["id"] == 4:
                environment = ReversedEnvironment()
            else:
                print("Fichier incompatible")
                return

            # On ajoute les données chargées
            environment.database = data[3]
            environment.load(data[1], data[2])
            game.active_environment = environment

            # On met à jour l'environnement actif
            game.environments_widget.addLoadEnvironment(environment, data[0]["name"])
            game.menu_active = False
        else:
            print("Interruption du chargement de la sauvegarde")
