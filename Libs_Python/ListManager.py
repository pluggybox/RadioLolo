# -*- coding: iso-8859-1 -*-

class ListManager():

    def __init__(self, fichier_liste_radios):
        self.liste_radios = []
        for ligne in open(fichier_liste_radios, 'r'):
            donnees_lues = ligne.split("|")
            self.liste_radios.append((donnees_lues[0], donnees_lues[1].strip()))

    def radios(self):
        return self.liste_radios