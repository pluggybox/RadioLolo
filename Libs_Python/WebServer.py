# -*- coding: iso-8859-1 -*-
from flask import Flask
from flask import render_template
from flask import request
import platform

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
SERVER_NAME = 'RadioLolo'

MODE_DEBUG  = True

if(platform.system() == 'Linux'):
    SERVER_PORT = 80
else:
    SERVER_PORT = 1234

#=======================================================================================================================
# Flask semble être utilisable seulement en module, pas dans une classe.
# On utilise des variables globales pour contourner cette limitation

app = Flask(SERVER_NAME, template_folder='HTML_templates')
player = None
liste_radios = None
liste_fichiers_MP3 = None

@app.route('/', methods=['GET', 'POST'])
def _HTTP_services():
    if request.method == 'POST':

        if request.form['submit'] == 'Lire':
            player.play(str(request.form['station']))
        elif request.form['submit'] == '+':
            player.modifier_volume(5)
        elif request.form['submit'] == '-':
            player.modifier_volume(-5)

    code_HTML_liste_radios = ''
    index_radio = 0
    for nom_radio, url_radio in liste_radios.radios():
        code_HTML_liste_radios += '<option value="' + str(index_radio) + '" '
        if(index_radio == player.index_lecture()):
            code_HTML_liste_radios += 'selected="selected"'
        code_HTML_liste_radios += '>' + nom_radio + '</option>'
        index_radio += 1

    code_HTML_liste_fichiers_MP3 = ''
    index_fichier_MP3 = 0
    for nom_acces, nom_affichage in liste_fichiers_MP3:
        code_HTML_liste_fichiers_MP3 += '<option value="' + str(index_fichier_MP3) + '" '
        if(index_fichier_MP3 == player.index_lecture()):
            code_HTML_liste_fichiers_MP3 += 'selected="selected"'
        code_HTML_liste_fichiers_MP3 += '>' + nom_affichage + '</option>'
        index_fichier_MP3 += 1

    return render_template('index.html', nom_de_la_page=SERVER_NAME, liste_stations=code_HTML_liste_fichiers_MP3.strip(),
                           volume='Volume: %d%%' % (player.lire_volume()),
                           etat_source_WEB='',
                           etat_source_MP3='')

#=======================================================================================================================
class WebServer():
    def __init__(self, musicPlayer, gestionnaire_liste_radios):
        global player, liste_radios, liste_fichiers_MP3
        player = musicPlayer
        liste_radios = gestionnaire_liste_radios
        liste_fichiers_MP3 = player.liste_fichiers_MP3()
        #for nom_radio, url_radio in liste_radios.radios():
        #    player.add(url_radio)
        for nom_acces, nom_affichage in liste_fichiers_MP3:
            player.add(nom_acces)
        player.play(player.index_lecture())

    def run(self):
        app.run(host='0.0.0.0', port=SERVER_PORT, debug=MODE_DEBUG)