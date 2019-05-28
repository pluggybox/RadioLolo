# -*- coding: iso-8859-1 -*-
from Libs_Python.WebServer import WebServer
from Libs_Python.MusicPlayer import MusicPlayer

if __name__ == '__main__':
    musicPlayer = MusicPlayer()
    webServer = WebServer(musicPlayer)
    webServer.run()
