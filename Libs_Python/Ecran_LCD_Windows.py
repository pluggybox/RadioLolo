# -*- coding: iso-8859-1 -*-
import serial

#==============================================================================
#                            C O N S T A N T E S
#==============================================================================
PORT_COM_INTERFACE_I2C = 'COM20'

#==============================================================================
class Ecran_LCD_Windows():

    def __init__(self, adresse_I2C_ecran):
        self.port_COM   = serial.Serial(port=PORT_COM_INTERFACE_I2C, baudrate=9600, timeout=0.2)
        self.adresse_I2C_ecran = adresse_I2C_ecran

    def envoyer_trame(self, adresse_registre, trame):
        taille_trame = len(trame)
        self.port_COM.write([0x55, self.adresse_I2C_ecran, adresse_registre, taille_trame] + trame)

    def __del__(self):
        self.port_COM.close()