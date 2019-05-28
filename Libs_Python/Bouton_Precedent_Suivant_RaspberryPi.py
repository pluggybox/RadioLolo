# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO


#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
NUMERO_BROCHE_PRECEDENT = 6
NUMERO_BROCHE_SUIVANT   = 5

#=======================================================================================================================
class Bouton_Precedent_Suivant_RaspberryPi():
    def __init__(self, callback_changement_etat_bouton):
        self.callback_changement_etat_bouton = callback_changement_etat_bouton
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NUMERO_BROCHE_PRECEDENT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(NUMERO_BROCHE_PRECEDENT, GPIO.RISING, callback=self._changement_etat_bouton_precedent, bouncetime=100)
        GPIO.setup(NUMERO_BROCHE_SUIVANT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(NUMERO_BROCHE_SUIVANT, GPIO.RISING, callback=self._changement_etat_bouton_suivant, bouncetime=100)

    def __del__(self):
        GPIO.cleanup()

    def _changement_etat_bouton_precedent(self, numero_broche):
        self.callback_changement_etat_bouton('-')

    def _changement_etat_bouton_suivant(self, numero_broche):
        self.callback_changement_etat_bouton('+')
