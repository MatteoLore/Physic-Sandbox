import pygame
import pymunk
from pymunk import Poly
from pymunk.pygame_util import DrawOptions

from sources.forms.circle import Circle
from sources.utils.colors import Colors
from sources.utils.database import Database
from sources.utils.texture import Texture


class Environment:
    """
    Classe héréditaire qui permet de définir un environnement, son espace de gravité ainsi que de nombreuses propriétés
    """

    def __init__(self):
        self.id = 0

        self.space = pymunk.Space()  # Définit l'espace de gravité
        self.space.gravity = (0, 981)  # Gravité (approximative) de la Terre adaptée au module pymunk
        self.gravity = (0, 981)  # gravité à ne pas toucher

        self.freeze = False
        self.strong_freeze = False
        self.science = False

        self.texture = Texture.BACKGROUND_MAIN

        self.initBox()

        self.database = None

    def initBox(self):
        """
        Définit la box de l'espace physique
        """
        static_lines = [
            # pymunk.Segment(self.space.static_body, (0, 0), (900, 0), 0), TOP
            pymunk.Segment(self.space.static_body, (900, 0), (900, 600), 0),
            pymunk.Segment(self.space.static_body, (900, 600), (0, 600), 0),
            pymunk.Segment(self.space.static_body, (0, 600), (0, 0), 0),
        ]
        for line in static_lines:
            line.elasticity = 1.0
            self.space.add(line)

    def update(self):
        """
        Met à jour l'espace
        """
        self.space.step(1 / 60.0)  # fréquence de mise à jour

    def checkClick(self, pos):
        """
        Si une figure est touchée, la figure est renvoyée
        """
        for shape in self.space.shapes:
            if isinstance(shape, Circle):
                if shape.isClicked(pos):
                    return shape
            elif isinstance(shape, Poly):
                if shape.isClicked(pos):
                    return shape
        return None

    def draw(self, surface):
        """
        Dessine l'espace en question
        """
        surface.fill(Colors.GRIS)  # On efface avant de redessiner

        background = pygame.image.load(self.texture)  # On applique le fond d'écran
        surface.blit(background, (0, 0))

        # Dessine chaque figure
        for shape in self.space.shapes:
            if isinstance(shape, pymunk.Segment):
                body = shape.body
                p1 = body.local_to_world(shape.a)
                p2 = body.local_to_world(shape.b)
                pygame.draw.lines(surface, Colors.NOIR, False, [p1, p2])
            elif isinstance(shape, Circle):
                shape.draw(surface)
                if self.science:
                    shape.printInfo(surface)
            elif isinstance(shape, Poly):
                shape.draw(surface)
                if self.science:
                    shape.printInfo(surface)

        for constraint in self.space.constraints:
            if isinstance(constraint, pymunk.DampedSpring):
                body1 = constraint.a
                center1 = body1.position
                for shape1 in body1.shapes:
                    if not isinstance(shape1, Circle):
                        center1 = center1 + shape1.getCenter()

                body2 = constraint.b
                center2 = body2.position
                for shape2 in body2.shapes:
                    if not isinstance(shape2, Circle):
                        center2 = center2 + shape2.getCenter()
                p1 = (int(center1[0]), int(center1[1]))
                p2 = (int(center2[0]), int(center2[1]))
                pygame.draw.line(surface, Colors.NOIR, p1, p2, 4)

        # Permet d'afficher les figures de manière brut, indisponible pour l'utilisateur, uniquement utile pour les développeurs
        # draw_options = DrawOptions(surface)
        # self.space.debug_draw(draw_options)

    def getFormsButtons(self):
        """
        Renvoie la liste des boutons-figures
        """
        return []

    def addShape(self, form, pos, texture):
        """
        Ajoute une figure en fonction de son nom
        """
        pass

    def stop(self, freeze=False):
        """
        Met en gel toutes activités dans l'espace
        """
        self.space.gravity = (0, 0)

        # Pour chaque forme, on enregistre les dernières force avant de les placer à 0 pour que la forme ne bouge plus
        for shape in self.space.shapes:
            if isinstance(shape, Circle):
                shape.last_force = shape.body.force
                shape.body.force = (0, 0)

                shape.last_velocity = shape.body.velocity
                shape.body.velocity = (0, 0)

                shape.last_rotation = shape.body.angular_velocity
                shape.body.angular_velocity = 0
            elif isinstance(shape, Poly):
                shape.last_force = shape.body.force
                shape.body.force = (0, 0)

                shape.last_velocity = shape.body.velocity
                shape.body.velocity = (0, 0)

                shape.last_rotation = shape.body.angular_velocity
                shape.body.angular_velocity = 0
        if freeze:
            self.freeze = False
        else:
            self.strong_freeze = True

    def play(self, freeze=False):
        """
        Dégel toutes activités dans l'espace
        """
        if freeze and self.strong_freeze:
            self.freeze = True
        else:
            self.space.gravity = self.gravity
            for shape in self.space.shapes:
                if isinstance(shape, Circle):
                    shape.body.force = shape.last_force
                    shape.body.velocity = shape.last_velocity
                    shape.body.angular_velocity = shape.last_rotation
                elif isinstance(shape, Poly):
                    shape.body.force = shape.last_force
                    shape.body.velocity = shape.last_velocity
                    shape.body.angular_velocity = shape.last_rotation
            self.strong_freeze = False
            self.freeze = False

    def reset(self):
        """
        Supprime toutes les formes présentes dans l'espace.
        """
        for shape in self.space.shapes:
            if isinstance(shape, Circle):
                self.space.remove(shape)
            elif isinstance(shape, Poly):
                self.space.remove(shape)
        for joint in self.space.constraints:
            self.space.remove(joint)

    def modeScience(self):
        """
        Active le mode scientifique
        """
        if self.science:
            self.science = False
        else:
            self.science = True

    def deleteShape(self, shape):
        """
        Supprime une forme donnée
        """
        for joint in shape.body.constraints:
            if joint in self.space.constraints:
                self.space.remove(joint)
        self.space.remove(shape)

    def link(self, form1, form2, rest_length=None):
        """
        Permet de liée de formes par un ressort
        """
        if form1 in self.space.shapes and form2 in self.space.shapes:
            if rest_length is None:
                rest_length = pymunk.Vec2d(form2.getCenter()[0], form2.getCenter()[1]) - pymunk.Vec2d(
                    form1.getCenter()[0], form1.getCenter()[1])
                rest_length = rest_length.length

            stiffness = 1000
            damping = 200000  # Rigidité du ressort

            # On récupère les points centraux par lequel le ressort sera attaché
            center1 = form1.getCenter()
            center2 = form2.getCenter()
            spring = pymunk.DampedSpring(form1.body, form2.body, center1, center2, rest_length, stiffness, damping)
            self.space.add(spring)

    # Database functions

    def save(self):
        """
        Enregistre l'environnement dans une base de donnée sql
        """

        # On stocke toutes les données dans plusieurs dictionnaires avant de les envoyer à la database
        data = {
            "id": self.id,
            "gravity": self.gravity[1],
        }

        joints_data = []
        joint_id = 1
        forms_data = []
        for shape in self.space.shapes:
            if shape.body.body_type == pymunk.Body.DYNAMIC:
                forms_data.append(
                    {
                        "id": shape.id,
                        "key": shape.key,
                        "posx": shape.body.position[0],
                        "posy": shape.body.position[1],
                        "mass": shape.body.mass,
                        "elasticity": shape.elasticity,
                        "friction": shape.friction,
                        "type": shape.type,
                        "texture": shape.texture_path
                    }

                )
                for joint in shape.body.constraints:
                    if isinstance(joint, pymunk.DampedSpring) and joint in self.space.constraints:
                        form1_id = shape.id

                        form2_id = None
                        for other_shape in self.space.shapes:
                            if other_shape.body == joint.b:
                                form2_id = other_shape.id
                                break

                        if form2_id is not None and not form1_id == form2_id:
                            joints_data.append(
                                {
                                    "id": joint_id,
                                    "form1_id": form1_id,
                                    "form2_id": form2_id,
                                    "length": joint.rest_length,
                                }
                            )
                            joint_id += 1

        if not self.database:
            self.database = Database()
            if self.database.active:
                self.database.saveEnvironment(data, forms_data, joints_data)
                return self.database
            else:
                self.database = None
                return None
        else:
            self.database.saveEnvironment(data, forms_data, joints_data)
            return None

    def load(self, forms_data, joints_data):
        """
        Charge un environnement à partir de données transmise
        """
        self.reset()

        for form_data in forms_data:  # On crée la forme et applique les propriétés enregistrées
            pos = (form_data["posx"], form_data["posy"])
            texture = form_data["texture"]
            shape = self.addShape(form_data["key"], pos, texture)
            shape.elasticity = form_data["elasticity"]
            shape.friction = form_data["friction"]
            shape.body.mass = form_data["mass"]
            if bool(form_data["type"]):
                shape.updateType(form_data["type"])

        for joint_data in joints_data:
            form1 = None
            form2 = None

            for shape in self.space.shapes:  # On lie les formes qui étaient liées
                if not isinstance(shape, pymunk.Segment):
                    if shape.id == joint_data["form1_id"]:
                        form1 = shape
                    elif shape.id == joint_data["form2_id"]:
                        form2 = shape

            if form1 and form2:
                self.link(form1, form2, rest_length=joint_data["length"])
