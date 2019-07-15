import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QFrame,QSplitter,QPushButton, QDialog,QWidget,QLabel
from PyQt5.QtGui import QIcon
from PyQt5 import QtMultimedia as Music
from PyQt5 import QtGui,QtCore
import os
import pygame
from PyQt5 import QtCore, QtGui, QtWidgets



class Desktop(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.pause_state= False
        self.play_state = False
        self.state=-1
        self.__layout=0
        self.file = os.listdir(os.getcwd() + '/music')
        self.current_i = 1
        self.count = len(self.file)
        pygame.init()
        self.music=pygame.mixer.Channel(0)
        self.now_play=None
        self.send = None
        self.add_button()
        self.initUI()
        self.open_file()
        self.open()
        self.next_music()
        self.play()
        self.previosly_music()

    def initUI(self):
        self.setStyleSheet('background-color:white')
        self.setGeometry(200,200,300,300)
        self.setWindowTitle('App')
        self.second=None
        self.show()


    def add_button(self):
        self.btn_play=QPushButton(self)
        self.btn_play.resize(30,30)
        self.btn_play.setStyleSheet('background-color: blue')
        self.btn_play.setIcon(QtGui.QIcon('icons8-circled-play-120.png'))
        self.btn_play.setIconSize(QtCore.QSize(40,40))
        self.btn_play.move(10,60)

        self.prev = QPushButton(self)
        self.prev.resize(30, 30)
        self.prev.setStyleSheet('background-color: blue')
        self.prev.setIcon(QtGui.QIcon('icons8-back-40 (копия).png'))
        self.prev.setIconSize(QtCore.QSize(40, 40))
        self.prev.move(160, 60)

        self.next = QPushButton(self)
        self.next.resize(30, 30)
        self.next.setStyleSheet('background-color: blue')
        self.next.setIcon(QtGui.QIcon('icons8-back-40 (копия).png'))
        self.next.setIconSize(QtCore.QSize(40, 40))
        self.next.move(190, 60)

        self.btn_stop=QPushButton(self)
        self.btn_stop.resize(30,30)
        self.btn_stop.setStyleSheet('background-color: blue')
        self.btn_stop.setIcon(QtGui.QIcon('pause-button-clipart-puase-708714-7248443.png'))
        self.btn_stop.setIconSize(QtCore.QSize(40,40))
        self.btn_stop.move(220,60)

    def open(self):
        self.btn_play.clicked.connect(self.play)
        self.btn_stop.clicked.connect(self.play)
        self.next.clicked.connect(self.play)
        self.prev.clicked.connect(self.play)

    def open_file(self):
        self.path = os.getcwd() + '/music/'

    def next_music(self):
        self.current_i += 1
        if self.current_i >= self.count:
            self.current_i = 0
        return self.file[self.current_i]

    def previosly_music(self):
        self.current_i -=1
        if self.current_i <= 0:
            self.current_i = self.count - 1
        return self.file[self.current_i]

    def play(self):
        self.now_play=self.file[self.current_i]
        self.append_music=pygame.mixer.Sound(self.path + self.file[self.current_i])
        self.send=self.sender()
        if self.send==self.btn_play:
            if self.play_state != True and self.pause_state != False:
                self.music.unpause()
            else:
                self.music.play(self.append_music)
            self.play_state = True
            self.pause_state = False

        if self.send==self.next:
            self.music.play(pygame.mixer.Sound(self.path + self.next_music()))
        if self.send == self.prev:
            self.music.play(pygame.mixer.Sound(self.path + self.previosly_music()))
        if self.send == self.btn_stop:
            self.music.pause()
            self.pause_state = True
            self.play_state = False
    
    

if __name__ == '__main__':

     app = QApplication(sys.argv)
     desktop=Desktop()
     sys.exit(app.exec_())
