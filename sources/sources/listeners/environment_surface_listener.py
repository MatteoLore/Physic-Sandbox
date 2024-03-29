class EnvironmentSurfaceListener:
    """
    Dirige les événements liés à la surface des environnements
    """

    def __init__(self, manager):
        self.manager = manager  # Centre d'écoute général

    def changeEnvironment(self, pos):
        """
        Change l'environnement de jeu
        """
        clicked_button = self.manager.game.environments_widget.checkClick((pos[0], pos[1] - 600))
        if clicked_button:  # Vérifie si un bouton-environnement est touché
            self.manager.game.updateEnvironment(clicked_button)
            self.manager.dispatchTutorial("change environnement")
