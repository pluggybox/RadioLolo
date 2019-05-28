# -*- coding: iso-8859-1 -*-
import platform

if(platform.system() == 'Linux'):
    from Bouton_Precedent_Suivant_RaspberryPi import Bouton_Precedent_Suivant_RaspberryPi as Bouton
else:
    from Bouton_Precedent_Suivant_Windows import Bouton_Precedent_Suivant_Windows as Bouton

class Bouton_Precedent_Suivant():
    def __init__(self, callback_nouvel_etat_bouton):
        bouton = Bouton(callback_nouvel_etat_bouton)
