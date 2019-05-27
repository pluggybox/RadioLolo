# -*- coding: iso-8859-1 -*-
from msvcrt import getch
from threading import Thread

#=======================================================================================================================
class ThreadLectureClavier(Thread):
    def __init__(self, callback_increment_sens_positif, callback_increment_sens_negatif):
        Thread.__init__(self)
        self.callback_increment_sens_positif = callback_increment_sens_positif
        self.callback_increment_sens_negatif = callback_increment_sens_negatif

    def run(self):
        self.boucler = True
        while self.boucler is True:
            touche_lue = getch()
            if(touche_lue == '+'):
                self.callback_increment_sens_positif()
            if(touche_lue == '-'):
                self.callback_increment_sens_negatif()

    def stop(self):
        self.boucler = False

#=======================================================================================================================
class CodeurIncremental_Windows():
    def __init__(self, callback_increment_sens_positif, callback_increment_sens_negatif):
        self.thread_LectureClavier = ThreadLectureClavier(callback_increment_sens_positif, callback_increment_sens_negatif)
        self.thread_LectureClavier.start()

    def __del__(self):
        self.thread_LectureClavier.stop()