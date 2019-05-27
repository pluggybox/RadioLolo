# -*- coding: iso-8859-1 -*-
import platform

if(platform.system() == 'Linux'):
    from CodeurIncremental_RaspberryPi import CodeurIncremental_RaspberryPi as Codeur
else:
    from CodeurIncremental_Windows import CodeurIncremental_Windows as Codeur

class CodeurIncremental():
    def __init__(self, val_min, val_max, increment=1):
        self.val_min = val_min
        self.val_max = val_max
        self.increment = increment
        self.valeur_du_codeur = self.val_min
        self.codeur = Codeur(self.callback_increment_sens_positif, self.callback_increment_sens_negatif)

    def callback_increment_sens_positif(self):
        self.valeur_du_codeur += self.increment
        self._saturer_valeur()

    def callback_increment_sens_negatif(self):
        self.valeur_du_codeur -= self.increment
        self._saturer_valeur()

    def _saturer_valeur(self):
        if(self.valeur_du_codeur < self.val_min):
            self.valeur_du_codeur = self.val_min
        if(self.valeur_du_codeur > self.val_max):
            self.valeur_du_codeur = self.val_max

    def lire(self):
        return self.valeur_du_codeur

    def forcer_valeur(self, valeur):
        self.valeur_du_codeur = valeur