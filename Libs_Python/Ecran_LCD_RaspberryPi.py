# -*- coding: iso-8859-1 -*-
from smbus import SMBus  # pip install smbus-cffi

# ==============================================================================
#                           C O N S T A N T E S
# ==============================================================================
LCD_BUS_ID = 1  # Numéro du bus I2C


# ==============================================================================
class Ecran_LCD_RaspberryPi():
    def __init__(self, adresse_I2C_ecran):
        self.adresse_I2C_ecran = adresse_I2C_ecran >> 1
        self.bus = SMBus()
        self.bus.open(LCD_BUS_ID)

    def envoyer_trame(self, adresse_registre, trame):
        self.bus.write_i2c_block_data(self.adresse_I2C_ecran, adresse_registre, trame)

    def __del__(self):
        try:
            self.bus.close()
        except:
            pass