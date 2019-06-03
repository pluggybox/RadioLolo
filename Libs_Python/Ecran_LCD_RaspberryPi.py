# -*- coding: iso-8859-1 -*-
from smbus import SMBus  # pip install smbus-cffi

# ==============================================================================
#                           C O N S T A N T E S
# ==============================================================================
LCD_BUS_ID = 1  # Numéro du bus I2C
LCD_ADDR = 0x63  # 0xC6 décalé de 1 bit vers la droite

CMD_REG = 0
CMD_SET_CURSOR = 3
CMD_CLEAR_SCREEN = 12
CMD_BACKLIGHT_ON = 19
CMD_BACKLIGHT_OFF = 20
CMD_WRITE = 32
CMD_HIDE_CURSOR = 4


# ==============================================================================
class LCD():
    def __init__(self):
        """ Constructeur """
        self.bus = SMBus()
        self.bus.open(LCD_BUS_ID)
        self.clear()
        self.on()
        self.bus.write_i2c_block_data(LCD_ADDR, CMD_REG, [CMD_HIDE_CURSOR])
        self.write('Lecture:', 1)
        self.write('Selection:', 3)

    def on(self):
        self.bus.write_i2c_block_data(LCD_ADDR, CMD_REG, [CMD_BACKLIGHT_ON])

    def off(self):
        self.bus.write_i2c_block_data(LCD_ADDR, CMD_REG, [CMD_BACKLIGHT_OFF])

    def clear(self):
        self.bus.write_i2c_block_data(LCD_ADDR, CMD_REG, [CMD_CLEAR_SCREEN])

    def write(self, text, line_num=1, col_num=1):
        self.bus.write_i2c_block_data(LCD_ADDR, CMD_REG, [CMD_SET_CURSOR, line_num, col_num])
        self.bus.write_i2c_block_data(LCD_ADDR, CMD_REG, [ord(char) for char in text] + [ord(' ') for i in range(0, (
                    20 - len(text) - col_num + 1))])

    def __del__(self):
        """ Destructeur """
        try:
            self.clear()
            self.off()
            self.bus.close()
        except:
            pass