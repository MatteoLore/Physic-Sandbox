import pygame
import pymunk
from pymunk.pygame_util import DrawOptions

from sources.environments.environment import Environment
from sources.forms.autogeometry_shape import AutogeometryShape
from sources.forms.circle import Circle
from sources.forms.rectangular import Rectangular
from sources.utils.colors import Colors
from sources.utils.database import Database
from sources.utils.texture import Texture
from sources.widgets.buttons.form_button import FormButton


class ReversedEnvironment(Environment):
    """
    Environnement avec la gravité inversée
    """

    def __init__(self):
        super().__init__()
        self.id = 4

        self.space.gravity = (0, -981)  # On inverse la gravité terrestre
        self.gravity = (0, -981)

        self.texture = Texture.BACKGROUND_REVERSED

    def initBox(self):
        static_lines = [
            pymunk.Segment(self.space.static_body, (0, 0), (900, 0), 0),
            pymunk.Segment(self.space.static_body, (900, 0), (900, 600), 0),
            pymunk.Segment(self.space.static_body, (0, 600), (0, 0), 0),
        ]
        for line in static_lines:
            line.elasticity = 1.0
            self.space.add(line)

    def getFormsButtons(self):
        """
        Renvoie la liste des boutons-figures
        """
        return [
            FormButton("ball", "Ballon", Texture.BASKET_BALL),
            FormButton("apple", "Pomme", Texture.APPLE),
            FormButton("stick", "Baton", Texture.STICK_WITH_LEAF),
            FormButton("water_bucket", "Seau d eau", Texture.WATER_BUCKET),
            FormButton("house", "Petite maison", Texture.HOUSE)
        ]

    def addShape(self, form, pos, texture):
        """
        Ajoute une figure en fonction de son nom
        """
        if form == "ball":
            return self.createBall(pos, texture)
        elif form == "apple":  # autogeometry
            return self.createApple(pos, texture)
        elif form == "stick":
            return self.createStickLeaf(pos, texture)
        elif form == "water_bucket":  # autogeometry
            return self.createBucket(pos, texture)
        elif form == "house":  # autogeometry
            return self.createHouse(pos, texture)

    def createBall(self, pos, texture):
        """
        Crée une balle
        """
        body = pymunk.Body(300, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        ball = Circle(identifier, "ball", body, 30, texture, elasticity=0.8, friction=0.5)

        self.space.add(body, ball)

        return ball

    def createBucket(self, pos, texture):
        """
        Crée un seau d'eau
        """
        body = pymunk.Body(800, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        bucket = AutogeometryShape(identifier, "water_bucket", body, texture, elasticity=0)

        self.space.add(body, bucket)

        return bucket

    def createHouse(self, pos, texture):
        """
        Crée une petite maison
        """
        body = pymunk.Body(100000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        house = AutogeometryShape(identifier, "house", body, texture, elasticity=0)

        self.space.add(body, house)

        return house

    def createApple(self, pos, texture):
        """
        Crée une pomme
        """
        body = pymunk.Body(150, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        apple = AutogeometryShape(identifier, "apple", body, texture, elasticity=0.2)

        self.space.add(body, apple)

        return apple

    def createStickLeaf(self, pos, texture):
        """
        Crée un bout de bois
        """
        body = pymunk.Body(350, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        stick_leaf = AutogeometryShape(identifier, "stick", body, texture, elasticity=0.4)

        self.space.add(body, stick_leaf)

        return stick_leaf
