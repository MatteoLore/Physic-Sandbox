import pymunk
from pymunk import Vec2d

from sources.environments.environment import Environment
from sources.forms.autogeometry_shape import AutogeometryShape
from sources.forms.circle import Circle
from sources.forms.rectangular import Rectangular
from sources.utils.texture import Texture
from sources.widgets.buttons.form_button import FormButton


class WaterEnvironment(Environment):
    """
    Environnement représentant l'eau
    """

    def __init__(self):
        super().__init__()
        self.id = 3

        self.texture = Texture.BACKGROUND_AQUA

        self.initBox()

    def initBox(self):
        """
        Définit la box de l'espace physique
        """
        static_lines = [
            pymunk.Segment(self.space.static_body, (0, 0), (900, 0), 0),
            pymunk.Segment(self.space.static_body, (900, 0), (900, 600), 0),
            pymunk.Segment(self.space.static_body, (900, 600), (0, 600), 0),
            pymunk.Segment(self.space.static_body, (0, 600), (0, 0), 0),
        ]
        for line in static_lines:
            line.elasticity = 0
            self.space.add(line)
        static_lines[1].elasticity = 0.2

    def draw(self, surface):
        """
        Dessine l'espace en question
        """
        super().draw(surface)
        for shape in self.space.shapes:
            self.add_drag(shape.body)
            self.add_buoyancy(shape, 1000)

    def add_drag(self, body, damping=5):
        """
        Applique une force de trainée
        """
        vitesse_relative = body.velocity
        # Ajouter une force de traînée proportionnelle à la vitesse relative
        force_drag = -damping * vitesse_relative
        force_drag /= body.mass
        body.apply_force_at_local_point(Vec2d(force_drag.x, force_drag.y), (0, 0))

    def add_buoyancy(self, shape, density_fluid):
        """
        Applique une force de flottaison
        """
        body = shape.body
        # volume = area * density_fluid

        diff_density = density_fluid - (shape.density*1000)
        # Vérifier si l'objet flotte (si sa densité est inférieure à celle du fluide)
        if diff_density > 0:
            # Calculer la force de flottabilité selon la poussée d'Archimède
            # force_buoyancy = volume * diff_density * -self.space.gravity * 0.01 Les valeurs sont trop hautes :(

            # Applique une force constante dans la direction opposée à la gravité pour faire remonter l'objet à la surface
            force_buoyancy = -self.space.gravity * body.mass * 2
            body.apply_force_at_local_point(force_buoyancy, (0, 0))

    def getFormsButtons(self):
        """
        Renvoie la liste des boutons-figures
        """
        return [
            FormButton("pebbles", "Cailloux", Texture.PEBBLES),
            FormButton("stick", "Baton", Texture.STICK),
            FormButton("fish", "Poisson", Texture.FISH),
            FormButton("diving_mask", "Masque de plongee", Texture.DIVING_MASK),
            FormButton("bucket", "Seau de plage", Texture.BUCKET),
        ]

    def addShape(self, form, pos, texture):
        """
        Ajoute une figure en fonction de son nom
        """
        if form == "fish":
            return self.createFish(pos, texture)
        elif form == "stick":
            return self.createStick(pos, texture)
        elif form == "pebbles":  # autogeometry
            return self.createPebbles(pos, texture)
        elif form == "diving_mask":  # autoogeometry
            return self.createDivingMask(pos, texture)
        elif form == "bucket":  # autogeometry
            return self.createBucket(pos, texture)

    def createFish(self, pos, texture):
        """
        Crée un cercle
        """
        body = pymunk.Body(800, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        fish = Circle(identifier, "fish", body, 50, texture, elasticity=0, friction=0.5)

        self.space.add(body, fish)

        return fish

    def createPebbles(self, pos, texture):
        """
        Crée un caillou
        """
        body = pymunk.Body(6000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        pebbles = AutogeometryShape(identifier, "pebbles", body, texture, elasticity=0)

        self.space.add(body, pebbles)

        return pebbles

    def createDivingMask(self, pos, texture):
        """
        Crée un masque de plongée
        """
        body = pymunk.Body(100, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        diving_mask = Rectangular(identifier, "diving_mask", body, (90, 50), texture, elasticity=0)

        self.space.add(body, diving_mask)

        return diving_mask

    def createBucket(self, pos, texture):
        """
        Crée un seau d'eau
        """
        body = pymunk.Body(6000, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        bucket = AutogeometryShape(identifier, "bucket", body, texture, elasticity=0)

        self.space.add(body, bucket)

        return bucket

    def createStick(self, pos, texture):
        """
        Crée un bout de bois
        """
        body = pymunk.Body(350, 1)
        body.position = pos

        identifier = len(self.space.shapes) + 1

        stick = Rectangular(identifier, "stick", body, (168, 22), texture, elasticity=0)

        self.space.add(body, stick)

        return stick
