# -*- coding: iso-8859-1 -*-
import wx
from threading import Thread

#=======================================================================================================================
#                           C O N S T A N T E S
#=======================================================================================================================
LARGEUR_FENETRE = 200
HAUTEUR_FENETRE = 100


_callback_increment_sens_positif = None
_callback_increment_sens_negatif = None

#=======================================================================================================================
class IHM(wx.Frame):

    def __init__(self, titre):
        wx.Frame.__init__(self, parent=None, title=titre, size=(LARGEUR_FENETRE, HAUTEUR_FENETRE))
        self.panel = wx.Panel(self)
        self.conteneur_principal = wx.BoxSizer(wx.HORIZONTAL)

        self.creer_bouton_moins(self.conteneur_principal)
        self.creer_bouton_plus(self.conteneur_principal)


        self.panel.SetSizer(self.conteneur_principal)
        self.Center()

    def creer_bouton_plus(self, conteneur):
        self.bouton_plus = wx.Button(self.panel, label='+')
        self.Bind(wx.EVT_BUTTON, self.callback_increment_sens_positif, self.bouton_plus)
        conteneur.Add(self.bouton_plus, flag=wx.RIGHT, border=8)

    def creer_bouton_moins(self, conteneur):
        self.bouton_moins = wx.Button(self.panel, label='-')
        self.Bind(wx.EVT_BUTTON, self.callback_increment_sens_negatif, self.bouton_moins)
        conteneur.Add(self.bouton_moins, flag=wx.RIGHT, border=8)

    def callback_increment_sens_positif(self, evenement):
        _callback_increment_sens_positif()

    def callback_increment_sens_negatif(self, evenement):
        _callback_increment_sens_negatif()

#=======================================================================================================================
class MonApplication(wx.App):
    def OnInit(self):
        fenetre = IHM(u"Codeur Incremental")
        fenetre.Show(True)
        self.SetTopWindow(fenetre)
        return True

#=======================================================================================================================
class ThreadLectureClavier(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = MonApplication()
        app.MainLoop()

#=======================================================================================================================
class CodeurIncremental_Windows():
    def __init__(self, callback_increment_sens_positif, callback_increment_sens_negatif):
        global _callback_increment_sens_positif, _callback_increment_sens_negatif
        _callback_increment_sens_positif = callback_increment_sens_positif
        _callback_increment_sens_negatif = callback_increment_sens_negatif
        self.thread_LectureClavier = ThreadLectureClavier()
        self.thread_LectureClavier.start()
