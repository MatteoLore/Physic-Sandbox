class FormsSurfaceListener:
    """
    Dirige les événements liés à la surface des formes
    """

    def __init__(self, manager):
        self.manager = manager  # Centre d'écoute général

    def setSelectedForm(self, pos):
        """
        Définit une figure sélectionnée.
        """
        clicked_button = self.manager.game.forms_widget.checkClick((pos[0] - 900, pos[1]))
        if clicked_button:
            self.manager.selected_form = clicked_button
            self.manager.mouse_tracker = clicked_button.texture_path

            if self.manager.link_form is not None:  # Si une figure était sélectionnée pour être liée, on la déselectionne
                self.manager.link = False
                self.manager.link_form.highlighted = False
            
            self.manager.dispatchTutorial("choisir forme")
