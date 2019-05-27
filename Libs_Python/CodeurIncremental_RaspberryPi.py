# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
NUMERO_BROCHE_CHANNEL_A = 19
NUMERO_BROCHE_CHANNEL_B = 26

#=======================================================================================================================
class CodeurIncremental_RaspberryPi():
    def __init__(self, callback_increment_sens_positif, callback_increment_sens_negatif):
        self.callback_increment_sens_positif = callback_increment_sens_positif
        self.callback_increment_sens_negatif = callback_increment_sens_negatif

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(NUMERO_BROCHE_CHANNEL_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(NUMERO_BROCHE_CHANNEL_A, GPIO.RISING, callback=self._IT_channel_A, bouncetime=10)
        GPIO.setup(NUMERO_BROCHE_CHANNEL_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __del__(self):
        GPIO.cleanup()

    def _IT_channel_A(self, numero_broche):
        if(GPIO.input(NUMERO_BROCHE_CHANNEL_B) == 0):
            self.callback_increment_sens_positif()
        else:
            self.callback_increment_sens_negatif()