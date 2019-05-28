# -*- coding: iso-8859-1 -*-
import os
import subprocess
import platform
from PersistantParameters import PersistantParameters, CLE_INDEX_RADIO, CLE_VOLUME, CLE_SOURCE
from CodeurIncremental import CodeurIncremental
from Bouton_2_etats import Bouton_2_etats

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
if(platform.system() == 'Linux'):
    MPC_COMMAND = 'mpc'
    PARAMETER_FILE = '/mnt/clef_USB/parameters.cfg'
    DIR_MP3_FILES = '/mnt/clef_USB/MP3/'
else:
    MPC_COMMAND = 'mpc.bat'
    PARAMETER_FILE = r'C:\Users\Public\parameters.cfg'
    DIR_MP3_FILES = r'C:\Users\Public\MP3\\'

#=======================================================================================================================

class MusicPlayer():

    def __init__(self):
        self.fichier_parametres = PersistantParameters(PARAMETER_FILE)
        self.parametres = self.fichier_parametres.lire()
        self.bouton_volume = CodeurIncremental(0, 100, increment=5, callback_nouvelle_valeur=self.nouvelle_valeur_du_codeur)
        self.bouton_source = Bouton_2_etats(self.nouvel_etat_du_bouton_source)
        self.clear()
        self.volume = self.parametres[CLE_VOLUME]
        self._run_command(['volume', str(self.volume)])
        self.bouton_volume.forcer_valeur(self.volume)

    def _run_command(self, command):
        cmd = [MPC_COMMAND] + command
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        return p.stdout.read()

    def add(self, url):
        self._run_command(['add', url])

    def clear(self):
        self._run_command(['clear'])

    def play(self, index_radio):
        self.parametres[CLE_INDEX_RADIO] = int(index_radio)
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

    def changer_volume(self, volume):
        self.volume = int(volume)
        self.parametres[CLE_VOLUME] = self.volume
        self._run_command(['volume', str(self.volume)])

    def lire_volume(self):
        return self.volume

    def lire_source_lecture(self):
        return self.parametres[CLE_SOURCE]

    def changer_source_lecture(self, source):
        self.parametres[CLE_SOURCE] = source

    def liste_fichiers_MP3(self):
        liste_fichiers = []
        filtre_extension = (".wav", ".mp3")
        for root, dirs, files in os.walk(DIR_MP3_FILES):
            for file in files:
                if file.lower().endswith(tuple(filtre_extension)):
                    nom_acces = os.path.join(root, file)
                    nom_affichage = nom_acces.replace(DIR_MP3_FILES, '')
                    liste_fichiers.append((nom_acces, nom_affichage))
        return liste_fichiers

    def sauver_parametres(self):
        self.fichier_parametres.ecrire(self.parametres)

    def nouvelle_valeur_du_codeur(self, valeur_du_codeur):
        self.changer_volume(valeur_du_codeur)

    def nouvel_etat_du_bouton_source(self, etat):
        if etat is True:
            self.changer_source_lecture('Web')
        else:
            self.changer_source_lecture('MP3')