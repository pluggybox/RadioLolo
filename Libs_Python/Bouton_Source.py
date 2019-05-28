# -*- coding: iso-8859-1 -*-
import platform

if(platform.system() == 'Linux'):
    from Bouton_Source_RaspberryPi import Bouton_Source_RaspberryPi as Bouton
else:
    from Bouton_Source_Windows import Bouton_Source_Windows as Bouton

class Bouton_Source():
    def __init__(self, callback_nouvel_etat_bouton):
        bouton = Bouton(callback_nouvel_etat_bouton)
