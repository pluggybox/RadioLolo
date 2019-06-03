# -*- coding: iso-8859-1 -*-
import os
import subprocess
import platform
from PersistantParameters import PersistantParameters, CLE_INDEX_RADIO, CLE_VOLUME, CLE_SOURCE
from CodeurIncremental import CodeurIncremental
from Bouton_Source import Bouton_Source
from Bouton_Precedent_Suivant import Bouton_Precedent_Suivant
from ListManager import ListManager
from Ecran_LCD import Ecran_LCD

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
if(platform.system() == 'Linux'):
    MPC_COMMAND = 'mpc'
    PARAMETER_FILE = '/mnt/clef_USB/parameters.cfg'
    DIR_MP3_FILES = '/mnt/clef_USB/MP3/'
    LISTE_RADIOS = '/mnt/clef_USB/liste_radios.txt'
else:
    MPC_COMMAND = 'mpc.bat'
    PARAMETER_FILE = r'C:\Users\Public\parameters.cfg'
    DIR_MP3_FILES = r'C:\Users\Public\MP3\\'
    LISTE_RADIOS = r'C:\Users\Public\liste_radios.txt'

#=======================================================================================================================

class MusicPlayer():

    def __init__(self):
        self.fichier_parametres = PersistantParameters(PARAMETER_FILE)
        self.parametres = self.fichier_parametres.lire()
        self.bouton_volume = CodeurIncremental(0, 100, increment=5, callback_nouvelle_valeur=self.nouvelle_valeur_du_codeur)
        self.bouton_source = Bouton_Source(self.nouvel_etat_du_bouton_source)
        self.bouton_precedent_suivant = Bouton_Precedent_Suivant(self.nouvel_etat_du_bouton_precedent_suivant)
        self.ecran = Ecran_LCD()
        self.clear()
        self.volume = self.parametres[CLE_VOLUME]
        self._run_command(['volume', str(self.volume)])
        self.bouton_volume.forcer_valeur(self.volume)

        gestionnaire_liste_radios = ListManager(LISTE_RADIOS)
        self.liste_radios = gestionnaire_liste_radios.radios()
        self.liste_fichiers_MP3 = self.liste_fichiers_MP3()
        self.changer_source_lecture(self.lire_source_lecture())
        self.play(0)

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
        self.index_lecture_en_cours = int(index_radio)
        self._run_command(['play', str(self.index_lecture_en_cours + 1)])
        self.mise_a_jour_ecran()

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
        self.mise_a_jour_ecran()

    def changer_volume(self, volume):
        self.volume = int(volume)
        self.parametres[CLE_VOLUME] = self.volume
        self._run_command(['volume', str(self.volume)])
        self.mise_a_jour_ecran()

    def lire_volume(self):
        return self.volume

    def lire_source_lecture(self):
        return self.parametres[CLE_SOURCE]

    def changer_source_lecture(self, source):
        self.parametres[CLE_SOURCE] = source
        self.clear()
        if(source == 'Web'):
            self.liste_en_cours = self.liste_radios
            for nom_radio, url_radio in self.liste_en_cours:
                self.add(url_radio)
        else:
            self.liste_en_cours = self.liste_fichiers_MP3
            for nom_acces, nom_affichage in self.liste_fichiers_MP3:
                self.add('file://' + nom_acces)
        self.play(0)

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

    def lire_liste_en_cours(self):
        return self.liste_en_cours

    def nouvel_etat_du_bouton_precedent_suivant(self, etat):
        index_lecture = self.index_lecture_en_cours

        if etat == '+':
            index_lecture += 1
            if(index_lecture >= len(self.liste_en_cours) ):
                index_lecture = 0

        if etat == '-':
            index_lecture -= 1
            if(index_lecture < 0 ):
                index_lecture = len(self.liste_en_cours) - 1

        self.play(index_lecture)

    def mise_a_jour_ecran(self):
        self.ecran.clear()
        titre = self.lire_source_lecture() + ': ' + self.lire_liste_en_cours()[self.index_lecture_en_cours][0].replace('\\', '').replace('/', '')
        print titre
        self.ecran.ecrire(titre)
        self.ecran.ecrire('Volume: %d%%'%(self.volume), 3, 1)