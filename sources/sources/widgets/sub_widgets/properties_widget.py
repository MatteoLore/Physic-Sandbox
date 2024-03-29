import pygame

from sources.utils.colors import Colors
from sources.utils.texture import Texture


class PropertiesWidget:
    """
    Classe qui permet l'affiche des propriétés d'une figure.
    """

    def __init__(self, figure):
        # Définition de la surface de la boîte de dialogue et des différentes options d'affichage
        self.properties_surface = pygame.Surface((300, 400))
        self.width = 300
        self.height = 400
        self.border_color = (0, 0, 0)
        self.font = pygame.font.Font(None, 24)

        # Position de la boîte de dialogue
        self.pos = ((pygame.display.get_surface().get_width() - self.width) // 2,
                    (pygame.display.get_surface().get_height() - self.height) // 2)

        # Figure liée à la boîte de dialogue
        self.figure = figure

        # Définition de la masse, rebond, status et frottement de la figure
        self.masse = figure.body.mass
        self.rebond = figure.elasticity
        self.frottement = figure.friction
        self.statut = figure.type

        self.buttons = {
            "Masse": {"plus": pygame.Rect(240, 160, 20, 20), "minus": pygame.Rect(120, 160, 20, 20)},
            "Rebond": {"plus": pygame.Rect(240, 200, 20, 20), "minus": pygame.Rect(120, 200, 20, 20)},
            "Frottement": {"plus": pygame.Rect(240, 240, 20, 20), "minus": pygame.Rect(120, 240, 20, 20)},
            "annuler": pygame.Rect(50, 350, 80, 30),
            "enregistrer": pygame.Rect(170, 350, 100, 30),
        }  # Dictionnaire des boutons présents

        self.status_buttons = {
            "dynamique": pygame.Rect(80, 300, 100, 30),
            "statique": pygame.Rect(180, 300, 100, 30),
        }  # Dictionnaire des boutons de status de la figure

    def draw(self, surface):
        """
        Affiche la boîte de dialogue
        """
        # Fond de la boîte
        background = pygame.image.load(Texture.BACKGROUND_ENVIRONMENT).convert()
        background = pygame.transform.scale(background, (self.width, self.height))
        self.properties_surface.blit(background, (0, 0))
        pygame.draw.rect(self.properties_surface, Colors.NOIR, self.properties_surface.get_rect(), 2)

        # Titre
        title = self.font.render("Propriétés", True, Colors.NOIR)
        text_rect = title.get_rect(center=(self.width // 2, 25))
        self.properties_surface.blit(title, text_rect)

        # Réprésentation de la figure
        forms_img = self.figure.texture
        if forms_img.get_width() > 100 or forms_img.get_height() > 75:
            forms_img = pygame.transform.scale(forms_img,
                                               (forms_img.get_width() // (5 / 3), forms_img.get_height() // (5 / 3)))
        img_rect = forms_img.get_rect(center=(self.width // 2, 75))
        self.properties_surface.blit(forms_img, img_rect)

        # Dessine les boutons, et leurs valeurs
        for label, button_rects in self.buttons.items():
            if label in ["annuler", "enregistrer"]:
                pygame.draw.rect(self.properties_surface, self.border_color, button_rects, 2)
                text_rendered = self.font.render(label.capitalize(), True, Colors.NOIR)
                text_rect = text_rendered.get_rect(center=button_rects.center)
                self.properties_surface.blit(text_rendered, text_rect)
            else:
                # Label de la valeur
                value_label_rendered = self.font.render(label, True, Colors.NOIR)
                value_label_rect = pygame.Rect(button_rects["minus"].x - 80, button_rects["minus"].y, 50, 20)
                value_label_text_rect = value_label_rendered.get_rect(center=value_label_rect.center)
                self.properties_surface.blit(value_label_rendered, value_label_text_rect)

                # Bouton "-"
                pygame.draw.rect(self.properties_surface, self.border_color, button_rects["minus"], 2)
                minus_text_rendered = self.font.render("-", True, Colors.NOIR)
                minus_text_rect = minus_text_rendered.get_rect(center=button_rects["minus"].center)
                self.properties_surface.blit(minus_text_rendered, minus_text_rect)

                # Valeur
                value = getattr(self, label.lower())

                value_rendered = self.font.render(f"{value:.1f}", True, Colors.NOIR)
                value_rect = pygame.Rect(button_rects["minus"].right + 5, button_rects["minus"].y, 80, 20)
                value_text_rect = value_rendered.get_rect(center=value_rect.center)
                self.properties_surface.blit(value_rendered, value_text_rect)

                # Bouton "+"
                pygame.draw.rect(self.properties_surface, self.border_color, button_rects["plus"], 2)
                plus_text_rendered = self.font.render("+", True, Colors.NOIR)
                plus_text_rect = plus_text_rendered.get_rect(center=button_rects["plus"].center)
                self.properties_surface.blit(plus_text_rendered, plus_text_rect)

        status_label_rendered = self.font.render("Statut", True, Colors.NOIR)
        status_label_rect = status_label_rendered.get_rect(center=(40, 312))
        self.properties_surface.blit(status_label_rendered, status_label_rect)

        for label, button_rect in self.status_buttons.items():
            if label == "dynamique" and self.statut == 0:
                pygame.draw.rect(self.properties_surface, Colors.ORANGE_ROUGE, button_rect, 2)
            elif label == "statique" and self.statut == 1:
                pygame.draw.rect(self.properties_surface, Colors.ORANGE_ROUGE, button_rect, 2)
            else:
                pygame.draw.rect(self.properties_surface, self.border_color, button_rect, 2)

            text_rendered = self.font.render(label, True, Colors.NOIR)
            text_rect = text_rendered.get_rect(center=button_rect.center)
            self.properties_surface.blit(text_rendered, text_rect)

        surface.blit(self.properties_surface, self.pos)

    def handle_events(self, event):
        """
        Prends en charge tous les événements propres à la boîte de dialogue
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            relative_pos = (pos[0] - self.pos[0], pos[1] - self.pos[1])
            for label, button_rects in self.buttons.items():
                if label not in ["annuler", "enregistrer"]:
                    if button_rects["minus"].collidepoint(relative_pos):
                        self.decrease_value(label)
                    elif button_rects["plus"].collidepoint(relative_pos):
                        self.increase_value(label)
                elif label == "enregistrer" and button_rects.collidepoint(relative_pos):
                    self.save()
                    return False

            for label, button_rect in self.status_buttons.items():
                if button_rect.collidepoint(relative_pos):
                    self.set_status(label)

            if self.buttons["annuler"].collidepoint(relative_pos) or self.buttons["enregistrer"].collidepoint(
                    relative_pos):
                return False
        return True

    def decrease_value(self, property_name):
        """
        Permet de réduire les valeurs des propriétés
        """
        if property_name == "Masse":
            if self.masse > self.calculate_masse():
                self.masse -= self.calculate_masse()
            elif self.masse == 10 or self.masse == 100 or self.masse == 1000:
                self.masse -= (self.masse / 10)
        elif property_name == "Rebond":
            if self.rebond > 0:
                self.rebond = max(self.rebond - 0.1, 0)
        elif property_name == "Frottement":
            if self.frottement > 0:
                self.frottement = max(self.frottement - 0.1, 0)

    def increase_value(self, property_name):
        """
        Permet d'augmenter les valeurs des propriétés
        """
        if property_name == "Masse":
            if self.masse < 100000:
                self.masse += self.calculate_masse()
        elif property_name == "Rebond":
            if self.rebond < 2:
                self.rebond = min(self.rebond + 0.1, 2)
        elif property_name == "Frottement":
            if self.frottement < 2:
                self.frottement = min(self.frottement + 0.1, 2)

    def calculate_masse(self):
        """
        Calcule la valeur d'ajout/retrait de la masse en fonction de cette dernière
        """
        if self.masse <= 9:
            return 1
        if self.masse <= 99:
            return 10
        elif self.masse <= 999:
            return 100
        elif self.masse <= 9999:
            return 1000
        else:
            return 5000

    def set_status(self, label):
        """
        Définit le status de la figure
        """
        if label == "dynamique":
            self.statut = 0
        elif label == "statique":
            self.statut = 1

    def save(self):
        """
        Met à jour les propriétés de la figure.
        """
        self.figure.elasticity = self.rebond
        self.figure.friction = self.frottement
        self.figure.body.mass = self.masse

        self.figure.updateType(self.statut)
