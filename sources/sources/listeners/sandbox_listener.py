import pymunk

from sources.widgets.sub_widgets.forms_options_widget import FormsOptionsWidget


class SandboxListener:
    """
    Dirige les événements liés à la surface de jeu (espace physique)
    """

    def __init__(self, manager):
        self.manager = manager  # Centre d'écoute général

    def leftDownClick(self, pos):
        """
        Fait apparaitre une figure, ou bien en sélectionne une à déplacer
        """
        if self.manager.selected_form:
            self.spawnForm(pos)
        elif self.manager.link and not self.manager.link_form and not self.manager.game.active_environment.checkClick(
                pos) is None:
            self.selectLinkForm(pos)
        elif self.manager.link and not self.manager.link_form is None and self.manager.game.active_environment.checkClick(pos):
            if not self.manager.link_form == self.manager.game.active_environment.checkClick(pos):
                self.linkForms(pos)
        elif self.manager.game.active_environment.checkClick(pos) and not self.manager.moved_form:
            self.moveForm(pos)
            self.manager.dispatchTutorial("move_form")

    def selectLinkForm(self, pos):
        """
        Sélectionne une figure à lier
        """
        self.manager.link_form = self.manager.game.active_environment.checkClick(pos)
        self.manager.link = True
        self.manager.link_form.highlighted = True

    def linkForms(self, pos):
        """
        Lie deux formes entre elles
        """
        self.manager.game.active_environment.link(self.manager.link_form,
                                                  self.manager.game.active_environment.checkClick(pos))

        # Remet à l'initiale les propriétés touchées par le lien
        self.manager.link_form.highlighted = False
        self.manager.link_form = None
        self.manager.link = False
        self.manager.game.link_active = False
        self.manager.mouse_tracker = None

    def leftUpClick(self):
        """
        Relâche la figure déplacée à son nouvel emplacement
        """
        if self.manager.moved_form:
            self.manager.game.active_environment.play(freeze=True)
            self.manager.moved_form = None

    def rightDownClick(self, pos):
        """
        Affiche les propriétés de la figure touchée
        """
        if self.manager.game.active_environment.checkClick(pos):
            selected_figure = self.manager.game.active_environment.checkClick(pos)
            if selected_figure:
                context_menu = FormsOptionsWidget(selected_figure, pos)
                context_menu.showContextMenu(context_menu, self.manager)
            self.manager.dispatchTutorial("deplacer forme")

    def motionCursor(self, pos):
        """
        Redéfinit la position de la figure déplacée
        """
        if self.manager.moved_form:
            for joint in self.manager.moved_form.body.constraints:
                if isinstance(joint, pymunk.PinJoint):
                    joint.b.position = pos
            self.manager.moved_form.body.position = pos

    def spawnForm(self, pos):
        """
        Fait apparaitre une figure
        """
        self.manager.game.active_environment.addShape(self.manager.selected_form.form, pos, self.manager.selected_form.texture_path)
        self.manager.selected_form = None
        self.manager.mouse_tracker = None

    def moveForm(self, pos):
        """
        Sélectionne une figure à déplacer
        """
        self.manager.moved_form = self.manager.game.active_environment.checkClick(pos)
        self.manager.game.active_environment.stop(freeze=True)
        self.manager.dispatchTutorial("deplacer forme")
