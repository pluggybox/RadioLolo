# -*- coding: iso-8859-1 -*-
import platform
from threading import Thread, RLock
from time import sleep

if(platform.system() == 'Linux'):
    from Ecran_LCD_RaspberryPi import Ecran_LCD_RaspberryPi as Bus_Ecran
else:
    from Ecran_LCD_Windows import Ecran_LCD_Windows as Bus_Ecran
    
#============================================================================== 
#                           C O N S T A N T E S    
#==============================================================================
ADRESSE_I2C_ECRAN       = 0xC6

REGISTRE_COMMANDE       = 0

CMD_SET_CURSOR          = 3
CMD_CLEAR_SCREEN        = 12
CMD_BACKLIGHT_ON        = 19
CMD_BACKLIGHT_OFF       = 20
CMD_WRITE               = 32
CMD_HIDE_CURSOR         = 4

TIMEOUT_ECRAN           = 5

#==============================================================================
verrou = RLock()
class ThreadTimeout(Thread):
    def __init__(self, fonction_ecran_OFF):
        Thread.__init__(self)
        self.fonction_ecran_OFF = fonction_ecran_OFF
        self.chrono = 0

    def reset(self):
        verrou.acquire()
        self.chrono = TIMEOUT_ECRAN
        verrou.release()

    def run(self):
        self.boucler = True
        while(self.boucler == True):
            if(self.chrono > 0):
                sleep(1.0)
                verrou.acquire()
                self.chrono -= 1
                if(self.chrono == 0):
                    self.fonction_ecran_OFF()
                verrou.release()

    def stop(self):
        self.boucler = False

#============================================================================== 
class Ecran_LCD():
    def __init__(self):
        """ Constructeur """   
        self.bus = Bus_Ecran(ADRESSE_I2C_ECRAN)
        self.threadTimeout = ThreadTimeout(self.timeout_ecran)
        self.threadTimeout.start()
        self.clear()
        self.off()
        self.cacher_curseur()


    def cacher_curseur(self):
        self.envoyer_trame([CMD_HIDE_CURSOR])

    def on(self):
        self.envoyer_trame([CMD_BACKLIGHT_ON])
        
    def off(self):
        self.envoyer_trame([CMD_BACKLIGHT_OFF])
        
    def clear(self):
        self.envoyer_trame([CMD_CLEAR_SCREEN])
        
    def ecrire(self, text, line_num=1, col_num=1):
        self.envoyer_trame([CMD_SET_CURSOR, line_num, col_num])
        self.envoyer_trame([ord(char) for char in text] + [ord(' ') for i in range(0, (20 - len(text) - col_num + 1))])


    def envoyer_trame(self, trame):
        self.bus.envoyer_trame(REGISTRE_COMMANDE, trame)
        self.bus.envoyer_trame(REGISTRE_COMMANDE, [CMD_BACKLIGHT_ON])
        self.threadTimeout.reset()

    def timeout_ecran(self):
        self.bus.envoyer_trame(REGISTRE_COMMANDE, [CMD_BACKLIGHT_OFF])

    def __del__(self):
        try:
            self.clear()
            self.off()
        except:
            pass              