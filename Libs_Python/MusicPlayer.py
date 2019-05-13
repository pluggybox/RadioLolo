# -*- coding: iso-8859-1 -*-
import subprocess
import platform
from PersistantParameters import PersistantParameters, CLE_INDEX_RADIO, CLE_VOLUME

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
if(platform.system() == 'Linux'):
    MPC_COMMAND = 'mpc'
    PARAMETER_FILE = '/mnt/clef_USB/parameters.cfg'
else:
    MPC_COMMAND = 'mpc.bat'
    PARAMETER_FILE = r'C:\Users\Public\parameters.cfg'

#=======================================================================================================================

class MusicPlayer():

    def __init__(self):
        self.fichier_parametres = PersistantParameters(PARAMETER_FILE)
        self.parametres = self.fichier_parametres.lire()
        self._run_command(['clear'])
        self.volume = self.parametres[CLE_VOLUME]
        self._run_command(['volume', str(self.volume)])

    def _run_command(self, command):
        cmd = [MPC_COMMAND] + command
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        return p.stdout.read()

    def add(self, url):
        self._run_command(['add', url])

    def play(self, index_radio):
        self.parametres[CLE_INDEX_RADIO] = int(index_radio)
        self.fichier_parametres.ecrire(self.parametres)
        numero_radio = int(index_radio) + 1
        self._run_command(['play', str(numero_radio)])

    def stop(self):
        self._run_command(['stop'])

    def index_lecture(self):
        return self.parametres[CLE_INDEX_RADIO]

    def modifier_volume(self, offset):
        str_offset = str(offset)
        if(offset > 0):
            str_offset = '+%d'%(offset)
        self._run_command(['volume', str_offset])
        self.volume = int(self._run_command(['volume']).split(':')[1].split('%')[0])
        self.parametres[CLE_VOLUME] = self.volume
        self.fichier_parametres.ecrire(self.parametres)


    def lire_volume(self):
        return self.volume
