import pygame
import pymunk
from pymunk import Poly
from pymunk.pygame_util import DrawOptions

from sources.environments.environment import Environment
from sources.forms.autogeometry_shape import AutogeometryShape
from sources.forms.circle import Circle
from sources.forms.isocele import Isocele
from sources.forms.rectangular import Rectangular
from sources.utils.colors import Colors
from sources.utils.database import Database
from sources.utils.texture import Texture
from sources.widgets.buttons.form_button import FormButton


class MarsEnvironment(Environment):
    """
    Environnement avec la gravité de Mars
    """

    def __init__(self):
        super().__init__()
        self.id = 2

        self.space.gravity = (0, 371)  # (981*3.71) / 9.81 → Gravité (approximative) de Mars adapté au module Pymunk
        self.gravity = (0, 371)

        self.texture = Texture.BACKGROUND_MARS  # Fond d'écran de l'espace

    def getFormsButtons(self):
        """
        Renvoie la liste des boutons-figures
        """
        return [
            FormButton("asteroid", "Asteroide", Texture.ASTEROID),
            FormButton("data_screen", "Ecran de donnees", Texture.DATA_SCREEN),
            FormButton("robot", "Robot", Texture.ROBOT),
            FormButton("technologic_object", "Object technologique", Texture.TECHNOLOGICAL_OBJECT),
            FormButton("rocket", "Fusee", Texture.ROCKET),
        ]

    def addShape(self, form, pos, texture):
        """
        Ajoute une figure en fonction de son nom
        """
        if form == "rocket":
            return self.createRocket(pos, texture)
        elif form == "technologic_object":
            return self.createTechnologicObject(pos, texture)
        elif form == "data_screen":
            return self.createDataScreen(pos, texture)
        elif form == "asteroid":  # Autogeometry a faire
            return self.createAsteroid(pos, texture)
        elif form == "robot":  # autogeometry a faire
            return self.createRobot(pos, texture)

    def createAsteroid(self, pos, texture):
        """
        Crée un astéroïde
        """
        body = pymunk.Body(50000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        asteroid = AutogeometryShape(identifier, "asteroid", body, texture, elasticity=0, friction=0.5)

        self.space.add(body, asteroid)

        return asteroid

    def createRobot(self, pos, texture):
        """
        Crée un robot
        """
        body = pymunk.Body(10000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        robot = AutogeometryShape(identifier, "robot", body, texture, elasticity=0, friction=0.5)

        self.space.add(body, robot)

        return robot

    def createRocket(self, pos, texture):
        """
        Crée une fusée
        """
        body = pymunk.Body(25000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        rocket = Isocele(identifier, "rocket", body, (80, 100), texture, elasticity=0)

        self.space.add(body, rocket)

        return rocket

    def createTechnologicObject(self, pos, texture):
        """
        Crée un objet technologique
        """
        body = pymunk.Body(5000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        cube = Rectangular(identifier, "technologic_object", body, (100, 100), texture, elasticity=0)

        self.space.add(body, cube)

        return cube

    def createDataScreen(self, pos, texture):
        """
        Crée un écran de données
        """
        body = pymunk.Body(2000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        screen = Rectangular(identifier, "data_screen", body, (100, 54), texture, elasticity=0)

        self.space.add(body, screen)

        return screen
