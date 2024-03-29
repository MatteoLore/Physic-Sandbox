class TutorialListener:
    """
    Dirige le tutoriel en fonction des événements réalisé
    """

    def __init__(self, manager):
        self.manager = manager
        self.current_step = -1

        self.steps = [{
            #1
            "text": "Salut, moi c'est M.Tuto\nJe t'accompagnerai tout le long du tutoriel !\n\n Cliques ici pour commencer:",
            "mask_area": [(manager.game.screen, (0, 0))],
            "position": (20, 20),
            "size": (300, 400)
        },
        {
            #2
            "text": "Tu peux naviguer entre les différents mondes en utilisant le bouton latéral en bas à gauche.\n\nPour changer de monde cliques tout simplement sur l'icône du monde qui t'intéresse !",
            "mask_area": [(manager.game.tools_surface, (850, 600)), (manager.game.sandbox, (0, 0)), (manager.game.forms_surface, (900, 0))],
            "position": (50, 50),
            "size": (150, 200)
        },

        {
            #3
            "text": "Tu peux également choisir l'objet que tu veux utiliser dans la barre à droite.\n\n Découvres l'ensemble des objets disponibles en utilisant les flèches noires !",
            "mask_area": [(manager.game.sandbox, (0, 0)), (manager.game.tools_surface, (850, 600)), (manager.game.environment_surface, (0, 600))],
            "position": (50, 50),
            "size": (150, 200)
        },

        {
            #4
            "text": "Tu vois les différents icônes en bas ?\nIls te seront très utils lorsque tu manipuleras les objets.\n\n-La CARTOUCHE te permet d'enregister tes modifications sur ce monde.\n\n-La FLECHE réinitialise le monde. Alors penses à sauvegarder !\n\n-La MAISON te renvoie à l'écran d'acceuil.\n\n-Le bouton PAUSE stop ou relance l'action en cours dans le monde. Il te sera util pour faire tes modifications.",
            "mask_area": [(manager.game.sandbox, (0, 0)), (manager.game.forms_surface, (900, 0)), (manager.game.environment_surface, (0, 600))],
            "position": (50, 50),
            "size": (150, 200)
        },
        {
            #5
            "text": "La CHAINE te permet de lier les objets.\nCliques sur l'un puis successivement sur l'autre pour voir apparaître un lien entre eux.",
            "mask_area": [(manager.game.sandbox, (0, 0)), (manager.game.forms_surface, (900, 0)), (manager.game.environment_surface, (0, 600))],
            "position": (50, 50),
            "size": (150, 200)
        },

        {
            #6
            "text": "Le bouton avec le MICROSCOPE te permet d'afficher les forces qui s'exercent EN TEMPS REEL sur chaque objet.\n\nAppuies de nouveau pour faire disparaitre les données.",
            "mask_area": [(manager.game.sandbox, (0, 0)), (manager.game.forms_surface, (900, 0)), (manager.game.environment_surface, (0, 600))],
            "position": (50, 50),
            "size": (150, 200)
        },

        {
            #7
            "text": "Passons maintenant au principal !\n\nUne fois l'objet déposé dans le monde, tu peux le déplacer de nouveau où tu le veux.\n\nTu peux également le supprimer ou changer ses propriétés en faisant un 'clic droit' avec la souris.\n\nAllons dans les paramètres !",
            "mask_area": [(manager.game.sandbox, (0, -295)), (manager.game.tools_surface, (850, 600)), (manager.game.forms_surface, (900, 0)), (manager.game.environment_surface, (0, 600))],
            "position": (20, 20),
            "size": (75, 100)
        },
        {
            #8
            "text": "Tu peux changer les propriétés propres à chacun des objets.\n\nJe te laisse découvrir :",
            "mask_area": [(manager.game.sandbox, (0, -450)), (manager.game.tools_surface, (850, 600)), (manager.game.forms_surface, (900, 0)), (manager.game.environment_surface, (0, 600))],
            "position": (20, 20),
            "size": (75, 100)
        },
        {
            #9
            "text": "Tu es maintenant prêt à utiliser notre logiciel 'Physique Sandbox' ! N'hesites pas à revenir me voir si tu n'as pas tous compris.\nBonne aventure !",
            "mask_area": [(manager.game.screen, (0, 0))],
            "position": (20, 20),
            "size": (150, 200)
        },
    ]

        self.events_steps = [{
            #1
            "tout": False
        },
            {
                #2
                "change environnement": False,
            },
            {
                #3
                "choisir forme": False
            },
            {
                #4
                "manipuler outils": False
            },
            {
                #5
                "manipuler lien": False
            },
            {
                #6
                "manipuler microscope": False
            },
            {
                #7
                "deplacer forme": False
            },
            {
                #8
                "proprietes forme": False
            },
            {
                #9
                "tout": False
            },
        ]

        self.nextStep()

    def eventTutorial(self, event):
        """
        Permet de valider un événement de l'étape actuelle s'il est réalisé.
        """
        for event_type in self.events_steps[self.current_step]:
            if (event_type == event):
                self.events_steps[self.current_step][event] = True
            elif (event_type == "*"):
                self.events_steps[self.current_step]["*"] = True
        self.checkEventsStep(self.events_steps[self.current_step])

    def checkEventsStep(self, step):
        """
        Vérifie si l'étape est réalisée entièrement, si oui, elle passe à la suivante
        """
        success = True
        for event in step:
            if not step[event]:
                success = False

        if success:
            self.nextStep()

    def nextStep(self):
        """
        Passe à l'étape suivante, en définissant les nouveaux événements à réaliser et le contenu de l'étape
        """
        self.current_step += 1
        if self.current_step >= len(self.steps)-1:
            self.manager.game.tutorial_active = False
            self.current_step = 0

        widget = self.manager.game.tutorial_widget
        widget.text = self.steps[self.current_step]["text"]
        widget.position = self.steps[self.current_step]["position"]
        widget.mask_area = self.steps[self.current_step]["mask_area"]
        widget.size = self.steps[self.current_step]["size"]


