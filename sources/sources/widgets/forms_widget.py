import pygame

from sources.utils.colors import Colors
from sources.utils.texture import Texture


class FormsWidget:
    """
    Classe qui permet l'affichage de la zone des figures
    """

    def __init__(self, surface, environment):
        self.surface = surface
        self.environment = environment

        # Liste des boutons-figures (en fonction de l'environnement)
        self.forms = self.environment.getFormsButtons()

        # Liste des boutons-figures qui seront affiché (max 3)
        self.forms_view = []

        self.spacing = 65  # Espace entre chaque bouton
        self.y_position = 40  # Position y de départ

        # Indice de départ de la liste des figures affichées.
        self.key_start = 0
        self.setViewList()

    def setEnvironment(self, environment):
        """
        Lorsque l'environnement est modifié, on met à jour l'affichage des formes assignées à ce dernier.
        """
        self.environment = environment
        self.forms = self.environment.getFormsButtons()
        self.key_start = 0
        self.forms_view = []
        self.setViewList()

    def setViewList(self):
        """
        Définit la liste des boutons-figures qui seront affichés
        """
        if len(self.forms) < 3:
            # Les figures peuvent toutes être affichées
            self.forms_view = self.forms
        else:  # Sinon, le nombres de figures est trop important, on limite à 3 figures affichées (avec un système de défilement)
            if self.key_start + 2 == len(self.forms):
                self.key_start = -2
            elif self.key_start == -(len(self.forms)):
                self.key_start = 0
            x = self.key_start

            button = [UpArrowButton(), self.forms[x], self.forms[x + 1], self.forms[x + 2], DownArrowButton()]  # On ajoute les fléches pour se déplacer
            self.forms_view = button

    def draw(self):
        """
        Dessine la zone où se situent les boutons-figures
        """
        self.surface.fill(Colors.BEIGE)  # On efface tout

        background = pygame.image.load(Texture.BACKGROUND_FORMS)  # On applique le fond d'écran
        self.surface.blit(background, (0, 0))

        y_offset = 0
        # On affiche chaque bouton en mettant à jour les coordonnés y
        for button in self.forms_view:
            if isinstance(button, DownArrowButton):
                button.rect.center = (self.surface.get_width() // 2, self.surface.get_height()-30)
            else:
                button.rect.center = (self.surface.get_width() // 2, self.y_position + y_offset)

            button.draw(self.surface)
            y_offset += button.rect.height + self.spacing

    def checkClick(self, pos):
        """
        Si un bouton-figure est touché, la figure est sélectionnée. Si un bouton de défilement est touché, la listeView est mise à jour.
        """
        for button in self.forms_view:
            if button.isClicked(pos):
                if isinstance(button, UpArrowButton):  # on diminue l'indice de départ de la liste d'affichage
                    self.key_start -= 1
                    self.setViewList()
                elif isinstance(button, DownArrowButton):  # on augmente l'indice de départ de la liste d'affichage
                    self.key_start += 1
                    self.setViewList()
                else:
                    return button


class UpArrowButton:
    """
    Fléche pointant vers le haut, ayant la fonction d'un bouton
    """

    def __init__(self):
        self.image = pygame.image.load(Texture.ROOT_GENERAL +"arrow_up.png")
        self.image = pygame.transform.scale(self.image, (90, 60))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)


class DownArrowButton:
    """
    Fléche pointant vers le bas, ayant la fonction d'un bouton
    """

    def __init__(self):
        self.image = pygame.image.load(Texture.ROOT_GENERAL +"arrow_down.png")
        self.image = pygame.transform.scale(self.image, (90, 60))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)
