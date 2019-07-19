import sys
import os
import time
import pygame
from PyQt5.QtWidgets import QFileDialog,QListView,QListWidget,QGridLayout,QMainWindow,QApplication,QSplitter,QPushButton,QSlider, QDialog,QWidget,QLabel
from PyQt5.QtGui import QIcon,QBrush, QImage, QPainter, QPixmap, QWindow
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QPixmap,QColor,QBrush
from PyQt5 import QtCore, QtGui, QtWidgets



class ChoiceFiles(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Please select files')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*wav);;Python Files (*.py)", options=options)
        if fileName:
            full_path = fileName
            return full_path

    

class Desktop(QWidget):
    pygame.init()
    play_state = False
    pause_state = False

    def __init__(self,parent=None):
        super().__init__(parent)
        self.state=-1
        self.total_s = 0
        self.file = [song for song in os.listdir(os.getcwd() + '/music') if song.endswith('.wav')]
        self.current_i = 0
        self.mute_state = False
        self.path = os.getcwd() + '/music/'
        self.count = len(self.file)
        self.current_vol = 99
        self.music=pygame.mixer.Channel(0)
        self.now_play=None
        self.send = None
        self.initUI()
        
    def initUI(self):
        self.list_widget()
        self.add_button()
        self.event_button()
        self.widget_volume()
        self.setStyleSheet('background-color:white')
        self.setGeometry(200,200,420,300)
        self.setWindowTitle('App')
        self.show()

    def add_button(self):
        self.btn_play=QPushButton(self)
        self.btn_play.resize(30,30)
        self.btn_play.setIcon(QtGui.QIcon(os.getcwd() + '/icons/play.png'))
        self.btn_play.setIconSize(QtCore.QSize(40,40))
        self.btn_play.move(10,60)

        self.prev = QPushButton(self)
        self.prev.resize(30, 30)
        self.prev.setIcon(QtGui.QIcon(os.getcwd() + '/icons/prev.png'))
        self.prev.setIconSize(QtCore.QSize(40, 40))
        self.prev.move(160, 60)

        self.next = QPushButton(self)
        self.next.resize(30, 30)
        self.next.setIcon(QtGui.QIcon(os.getcwd() + '/icons/next.png'))
        self.next.setIconSize(QtCore.QSize(40, 40))
        self.next.move(190,60)
        
        self.btn_stop=QPushButton(self)
        self.btn_stop.resize(30,30)
        self.btn_stop.setIcon(QtGui.QIcon(os.getcwd() + '/icons/pause.png'))
        self.btn_stop.setIconSize(QtCore.QSize(40,40))
        self.btn_stop.move(220,60)

    def event_button(self):
        self.btn_play.clicked.connect(self.play)
        self.btn_stop.clicked.connect(self.play)
        self.next.clicked.connect(self.play)
        self.prev.clicked.connect(self.play)

    @property
    def next_music(self):
        self.current_i += 1
        if self.current_i >= self.count:
            self.current_i = 0
        return self.file[self.current_i]

    @property
    def previosly_music(self):
        self.current_i -=1
        if self.current_i < 0:
            self.current_i = self.count - 1
        return self.file[self.current_i]

    def play(self):
        self.append_music=pygame.mixer.Sound(self.path + self.file[self.current_i])
        self.now_play = self.append_music
        self.send=self.sender()
        self.duration_song = 0
        if self.send==self.btn_play:
            if self.play_state != True and self.pause_state != False:
                self.music.unpause()
            else:
                self.music.play(self.append_music)
            self.play_state = True
            self.duration_song = self.music.get_sound().get_length()
            
        elif self.send==self.next:
            self.music.play(pygame.mixer.Sound(self.path + self.next_music))
            self.duration_song = self.music.get_sound().get_length()

        elif self.send == self.prev:
            self.music.play(pygame.mixer.Sound(self.path + self.previosly_music))
            self.duration_song = self.music.get_sound().get_length()
           
        elif self.send == self.btn_stop:
            self.start_timer = False
            self.music.pause()
            self.pause_state = True
            self.play_state = False
        elif self.send == self.volume:
            try:
                if self.mute_state == False:
                    self.current_vol = self.music.get_sound().set_volume(0)
                    self.volume.setIcon(QtGui.QIcon(os.getcwd() + '/icons/mute.png'))
                    self.mute_state = True
                elif self.mute_state == True:
                    self.current_vol = self.music.get_sound().set_volume(99)
                    self.volume.setIcon(QtGui.QIcon(os.getcwd() + '/icons/two.png'))
                    self.mute_state = False
            except: 
                self.music.play(pygame.mixer.Sound( ChoiceFiles().openFileNameDialog()))
        self.play_check(self.current_i)

    def play_check(self,current):
        for num, song in enumerate(self.file):
            if num == current:
                continue # already playing
            next_turn = pygame.mixer.Sound(self.path + '/' + song)
            self.music.queue(next_turn)

    def widget_volume(self):
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(True)
        sld.setGeometry(270, 65, 60, 25)
        sld.setValue(99)
        sld.valueChanged[int].connect(self._changeValue)
        self.volume=QPushButton(self)
        self.volume.resize(20,20)
        self.volume.setIcon(QtGui.QIcon(os.getcwd() + '/icons/two.png'))
        self.volume.setIconSize(QtCore.QSize(15,15))
        self.volume.clicked.connect(self.play)
        self.volume.move(350,65)

    def _changeValue(self,value):
        try:
            if self.play_state == True:
                current_vol = self.music.get_sound().get_volume()
                if value == 0:
                    self.volume.setIcon(QtGui.QIcon(os.getcwd() + '/icons/mute.png'))
                elif value < 30:
                    self.volume.setIcon(QtGui.QIcon(os.getcwd() + '/icons/once.png'))
                elif value > 30:
                    self.volume.setIcon(QtGui.QIcon(os.getcwd() + '/icons/two.png'))
                change_vol = float(value / 100)
                current_vol = self.music.get_sound().set_volume(change_vol)
        except: 
            self.music.play(pygame.mixer.Sound( ChoiceFiles().openFileNameDialog())) 

    def list_widget(self):
        layout = QGridLayout()
        layout.setRowStretch(0, 6)
        layout.setRowStretch(1, 8)
        self.setLayout(layout)
        self.listwidget = QListWidget()
        for num,song in enumerate(self.file):
            self.listwidget.insertItem(num,song)
        self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget,1,0,1,0)
        
    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        select_song = item.text()
        self.current_i = self.file.index(select_song)
        song = pygame.mixer.Sound(self.path + self.file[self.current_i])
        self.music.play(song)
        
    
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    desktop=Desktop()
    sys.exit(app.exec_())
