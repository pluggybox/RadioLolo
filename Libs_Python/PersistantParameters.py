# -*- coding: iso-8859-1 -*-
import os
import pickle

INDEX_RADIO = "Index Radio"

class PersistantParameters():

    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier
        if not os.path.isfile(self.nom_fichier):
            self._creer_fichier_par_defaut()

    def _creer_fichier_par_defaut(self):
        self.parametres= {
            INDEX_RADIO: 0
        }
        self._sauver()

    def _sauver(self):
        with open(self.nom_fichier, 'wb') as fichier:
            pickle.dump(self.parametres, fichier)

    def lire(self):
        with open(self.nom_fichier, 'rb') as fichier:
            self.parametres = pickle.load(fichier)
        return self.parametres

    def ecrire(self, parametres):
        self.parametres = parametres
        self._sauver()