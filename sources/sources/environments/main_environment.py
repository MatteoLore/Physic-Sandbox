import pymunk

from sources.environments.environment import Environment
from sources.forms.circle import Circle
from sources.forms.triangle import Triangle
from sources.utils.texture import Texture
from sources.widgets.buttons.form_button import FormButton
from sources.forms.rectangular import Rectangular


class MainEnvironment(Environment):
    """
    Environnement principal, gravité de la terre
    """

    def __init__(self):
        super().__init__()
        self.id = 1

    def getFormsButtons(self):
        """
        Renvoie la liste des boutons-figures
        """
        return [
            FormButton("ball", "Balle", Texture.BALL),
            FormButton("cube", "Cube", Texture.CUBE),
            FormButton("square", "Equerre", Texture.SQUARE),
            FormButton("pile", "Pile", Texture.BATTERY),
            FormButton("ruler", "Regle", Texture.RULER),
            FormButton("book", "Livre", Texture.BOOK),
        ]

    def addShape(self, form, pos, texture):
        """
        Ajoute une figure en fonction de son nom
        """
        if form == "ball":
            return self.createBall(pos, texture)
        elif form == "square":
            return self.createSquare(pos, texture)
        elif form == "book":
            return self.createBook(pos, texture)
        elif form == "pile":
            return self.createBattery(pos, texture)
        elif form == "ruler":
            return self.createRuler(pos, texture)
        elif form == "cube":
            return self.createCube(pos, texture)

    def createBall(self, pos, texture):
        """
        Crée un cercle
        """
        body = pymunk.Body(250, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        circle = Circle(identifier, "ball", body, 15, texture, elasticity=0.8, friction=0.5)

        self.space.add(body, circle)

        return circle

    def createSquare(self, pos, texture):
        """
        Crée une équerre
        """
        body = pymunk.Body(600, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        triangle = Triangle(identifier, "square", body, (156, 94), texture, elasticity=0)

        self.space.add(body, triangle)

        return triangle

    def createBook(self, pos, texture):
        """
        Crée un livre
        """
        body = pymunk.Body(1000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        book = Rectangular(identifier, "book", body, (60, 80), texture, elasticity=0)

        self.space.add(body, book)

        return book

    def createRuler(self, pos, texture):
        """
        Crée une règle
        """
        body = pymunk.Body(230, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        ruler = Rectangular(identifier, "ruler", body, (30, 100), texture, elasticity=0)

        self.space.add(body, ruler)

        return ruler

    def createBattery(self, pos, texture):
        """
        Crée une pile
        """
        body = pymunk.Body(800, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        battery = Rectangular(identifier, "battery", body, (50, 100), texture, elasticity=0)

        self.space.add(body, battery)

        return battery

    def createCube(self, pos, texture):
        """
        Crée un cube
        """
        body = pymunk.Body(2000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        cube = Rectangular(identifier, "cube", body, (110, 110), texture, elasticity=0)

        self.space.add(body, cube)

        return cube
