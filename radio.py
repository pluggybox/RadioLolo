import os
from Libs_Python.WebServer import WebServer
from Libs_Python.MusicPlayer import MusicPlayer
from Libs_Python.ListManager import ListManager

LISTE_RADIOS = '/mnt/clef_USB/liste_radios.txt'

if __name__ == '__main__':
    musicPlayer = MusicPlayer()
    gestionnaire_liste_radios = ListManager(LISTE_RADIOS)
    webServer = WebServer(musicPlayer, gestionnaire_liste_radios)
    webServer.run()
