# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO


#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
NUMERO_BROCHE           = 13
FILTRE_ANTI_REBONDS     = 300

#=======================================================================================================================
class Bouton_Source_RaspberryPi():
    def __init__(self, callback_changement_etat_bouton):
        self.callback_changement_etat_bouton = callback_changement_etat_bouton
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NUMERO_BROCHE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(NUMERO_BROCHE, GPIO.BOTH, callback=self._changement_etat_bouton, bouncetime=FILTRE_ANTI_REBONDS)

    def __del__(self):
        GPIO.cleanup()

    def _changement_etat_bouton(self, numero_broche):
        if (GPIO.input(NUMERO_BROCHE) == 0):
            self.callback_changement_etat_bouton(False)
        else:
            self.callback_changement_etat_bouton(True)