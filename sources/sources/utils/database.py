import os
import sqlite3
import tkinter as tk
from tkinter import filedialog


class Database:
    """
    Classe qui permet de créer et diriger une base de données SQL
    """

    def __init__(self, file=None):
        self.active = True
        if not file: # si aucun fichier n'est reliée à la classe, on en crée un
            file = self.createFile()
            self.active = not isinstance(file, tuple)
            self.file = file
        else:
            self.file = file

        if self.active:  # si le fichier est valide, on initialise le module sql
            self.connexion = sqlite3.connect(self.file)
            self.cursor = self.connexion.cursor()
            self.initTables()
        else:
            print("Interruption de la création de la sauvegarde")

    def initTables(self):
        """
        Définit les tables sql
        """
        sql_request = [
            '''
                    CREATE TABLE IF NOT EXISTs Environment (
                    id INTEGER PRIMARY KEY,
                    gravity INTEGER NOT NULL,
                    name TEXT NOT NULL 
                    );
                    ''',
            '''
                    CREATE TABLE IF NOT EXISTs Forms (
                    id INTEGER PRIMARY KEY,
                    key TEXT NOT NULL,
                    posx REAL NOT NULL ,
                    posy REAL NOT NULL, 
                    mass INTEGER NOT NULL,
                    elasticity REAL NOT NULL,
                    friction REAL NOT NULL,
                    type INTEGER NOT NULL,
                    texture TEXT NOT NULL
                    );
                    ''',
            '''
                    CREATE TABLE IF NOT EXISTs Joints (
                    id INTEGER PRIMARY KEY,
                    form1_id INTEGER REFERENCES Forms(id),
                    form2_id INTEGER REFERENCES Forms(id),
                    length REAL NOT NULL
                    );
                    ''',
        ]

        # On exécute chaque requête sql
        for request in sql_request:
            self.cursor.execute(request)
            self.connexion.commit()

    def saveEnvironment(self, environment_data, forms_data, joints_data):
        """
        Sauvegarde les données dans la base de données.
        """
        # On supprime tout au préalable
        self.cursor.execute("DELETE FROM Environment")
        self.cursor.execute("DELETE FROM Forms")
        self.cursor.execute("DELETE FROM Joints")
        self.connexion.commit()

        # On insère les propriétés de l'environnement
        self.cursor.execute("INSERT INTO Environment (id, gravity, name) VALUES (?, ?, ?)",
                            (environment_data['id'], environment_data['gravity'], Database.getFileName(self.file)))
        self.connexion.commit()

        # On insère les formes et leurs propriétés
        if forms_data:
            for form_data in forms_data:
                self.cursor.execute("INSERT INTO Forms (id, key, posx, posy, mass, elasticity, friction, type, texture) "
                                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (form_data['id'], form_data['key'], form_data['posx'], form_data['posy'],
                                     form_data['mass'], form_data['elasticity'], form_data['friction'], form_data['type'], form_data["texture"]))
            self.connexion.commit()

        # On insère les liens entre formes
        if joints_data:
            for joint_data in joints_data:
                self.cursor.execute("INSERT INTO Joints (id, form1_id, form2_id, length) "
                                    "VALUES (?, ?, ?, ?)",
                                    (joint_data['id'], joint_data['form1_id'], joint_data['form2_id'], joint_data["length"]))
            self.connexion.commit()



    def createFile(self):
        """
        Ouvre une boîte de dialogue pour créer un fichier .sandbox et le renvoie
        """
        # on définit une fenêtre Tkinter, avec certaines spécificités, puis on l'ouvre
        root = tk.Tk()
        root.withdraw()
        nom_fichier = filedialog.asksaveasfilename(title="Enregistrer la sauvegarde",
                                                   filetypes=[("Fichiers Sandbox", "*.sandbox")],
                                                   defaultextension=".sandbox")
        root.destroy()
        return nom_fichier

    @staticmethod
    def selectFile():
        """
        Ouvre une boîte de dialogue pour choisir un fichier .sandbox et le renvoie
        :return:
        """
        # on définit une fenêtre Tkinter, avec certaines spécificités, puis on l'ouvre
        root = tk.Tk()
        root.withdraw()
        nom_fichier = filedialog.askopenfilename(
            title="Sélectionner un fichier à charger",
            filetypes=[("Fichiers Sandbox", "*.sandbox")]
        )
        root.destroy()

        return nom_fichier

    @staticmethod
    def loadEnvironment(file_path=None):
        """
        Charge les données d'un environnement à partir des données de la base de données sql
        """
        if file_path is None:  # Si aucun fichier n'est liée, on en choisit 1
            file_path = Database.selectFile()
        if not file_path: # Si le fichier n'est pas valide, on s'arrête ici
            return None

        connexion = sqlite3.connect(file_path)
        cursor = connexion.cursor()

        cursor.execute("SELECT * FROM Environment")
        environment_data = cursor.fetchone()

        # Charge les données de l'environnement
        environment = {
            "id": environment_data[0],
            "gravity": environment_data[1],
            "name": Database.getFileName(file_path)
        }

        # Charge les données des formes
        cursor.execute("SELECT * FROM Forms")
        forms_data = cursor.fetchall()
        forms = []
        for form_data in forms_data:
            form = {
                "id": form_data[0],
                "key": form_data[1],
                "posx": form_data[2],
                "posy": form_data[3],
                "mass": form_data[4],
                "elasticity": form_data[5],
                "friction": form_data[6],
                "type": form_data[7],
                "texture": form_data[8]
            }
            forms.append(form)

        # Charge les données des joints
        cursor.execute("SELECT * FROM Joints")
        joints_data = cursor.fetchall()
        joints = []
        for joint_data in joints_data:
            joint = {
                "id": joint_data[0],
                "form1_id": joint_data[1],
                "form2_id": joint_data[2],
                "length": joint_data[3]
            }
            joints.append(joint)

        connexion.close()

        return environment, forms, joints, Database(file_path)

    @staticmethod
    def getFileName(file):
        """
        Permet de récupérer le nom d'un fichier, et le renvoie
        """
        file = os.path.basename(file)
        file_name, file_extension = os.path.splitext(file)  # sépare l'extension et le nom du fichier
        return file_name




