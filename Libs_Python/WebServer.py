# -*- coding: iso-8859-1 -*-
from flask import Flask
from flask import render_template
from flask import request
import platform

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
SERVER_NAME = 'RadioLolo'

MODE_DEBUG  = False

if(platform.system() == 'Linux'):
    SERVER_PORT = 80
else:
    SERVER_PORT = 1234

#=======================================================================================================================
# Flask semble être utilisable seulement en module, pas dans une classe.
# On utilise des variables globales pour contourner cette limitation

app = Flask(SERVER_NAME, template_folder='HTML_templates')
player = None

@app.route('/', methods=['GET', 'POST'])
def _HTTP_services():
    traitement_methode_POST()
    code_HTML_liste, image_MP3, image_WEB = traitement_source()

    str_mode_debug = ''
    if MODE_DEBUG is True:
        str_mode_debug = '(DEBUG)'

    return render_template('index.html', nom_de_la_page=SERVER_NAME, liste_stations=code_HTML_liste.strip(),
                           volume='%d%%' % (player.lire_volume()),
                           mode_DEBUG=str_mode_debug,
                           image_WEB=image_WEB,
                           image_MP3=image_MP3,
                           valeur_du_bouton = player.lire_volume())


def traitement_source():
    source = player.lire_source_lecture()
    image_WEB = '/static/logo_WEB.jpg'
    image_MP3 = '/static/logo_MP3.jpg'
    if (source == 'Web'):
        image_WEB = '/static/logo_WEB_valide.jpg'
        code_HTML_liste = traitement_WEB()
    else:
        image_MP3 = '/static/logo_MP3_valide.jpg'
        code_HTML_liste = traitement_MP3()
    return code_HTML_liste, image_MP3, image_WEB


def traitement_methode_POST():
    if request.method == 'POST':
        if 'changer_volume' in request.form.keys():
            player.changer_volume(request.form['changer_volume'])

        elif 'Bouton_MP3.x' in request.form.keys():
            player.changer_source_lecture('MP3')

        elif 'Bouton_WEB.x' in request.form.keys():
            player.changer_source_lecture('Web')

        elif 'Play' in request.form.keys():
            player.play(str(request.form['station']))

        elif 'Save.x' in request.form.keys():
            player.sauver_parametres()

def traitement_WEB():
    code_HTML_liste = ''
    index_radio = 0
    for nom_radio, url_radio in player.lire_liste_en_cours():
        code_HTML_liste += '<option value="' + str(index_radio) + '" '
        if (index_radio == player.index_lecture()):
            code_HTML_liste += 'selected="selected"'
        code_HTML_liste += '>' + nom_radio + '</option>'
        index_radio += 1
    return code_HTML_liste

def traitement_MP3():
    code_HTML_liste = ''
    index_fichier_MP3 = 0
    for nom_acces, nom_affichage in  player.lire_liste_en_cours():
        code_HTML_liste += '<option value="' + str(index_fichier_MP3) + '" '
        if (index_fichier_MP3 == player.index_lecture()):
            code_HTML_liste += 'selected="selected"'
        code_HTML_liste += '>' + nom_affichage + '</option>'
        index_fichier_MP3 += 1
    return code_HTML_liste

#=======================================================================================================================
class WebServer():
    def __init__(self, musicPlayer):
        global player
        player = musicPlayer

    def run(self):
        app.run(host='0.0.0.0', port=SERVER_PORT, debug=MODE_DEBUG)