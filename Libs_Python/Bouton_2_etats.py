# -*- coding: iso-8859-1 -*-
import platform

if(platform.system() == 'Linux'):
    from Bouton_2_etats_RaspberryPi import Bouton_2_etats_RaspberryPi as Bouton
else:
    from Bouton_2_etats_Windows import Bouton_2_etats_Windows as Bouton

class Bouton_2_etats():
    def __init__(self, callback_nouvel_etat_bouton):
        bouton = Bouton(callback_nouvel_etat_bouton)
