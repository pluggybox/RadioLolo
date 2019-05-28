# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO


#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
NUMERO_BROCHE = 13

#=======================================================================================================================
class Bouton_2_etats_RaspberryPi():
    def __init__(self, callback_changement_etat_bouton):
        self.callback_changement_etat_bouton = callback_changement_etat_bouton
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NUMERO_BROCHE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(NUMERO_BROCHE, GPIO.RISING, callback=self._IT_appui, bouncetime=10)
        GPIO.add_event_detect(NUMERO_BROCHE, GPIO.FALLING, callback=self._IT_relachement, bouncetime=10)

    def __del__(self):
        GPIO.cleanup()

    def _IT_appui(self, numero_broche):
        self.callback_changement_etat_bouton(True)

    def _IT_relachement(self, numero_broche):
        self.callback_changement_etat_bouton(False)
