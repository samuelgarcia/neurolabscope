# -*- coding: utf-8 -*-
"""
Neurolabscope mainwindow.
"""

from PyQt4 import QtCore,QtGui
import os


from pyacq import StreamHandler, FakeMultiSignals, RawDataRecording
from pyacq.gui import Oscilloscope

from .guiutil import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent  = None):
        QtGui.QMainWindow.__init__(self, parent = parent)
        
        self.setWindowTitle(u'Simple acquisition system')
        self.setWindowIcon(QtGui.QIcon(':/neurolabscope.png'))
        self.setDockNestingEnabled(True)
        
        self.setAnimated(False)

        self.createActions()
        #~ self.createMenus()
        self.createToolBars()
        
        self.devices_conf  = None
        self.devices = [ ]
        self.docks = [ ]
        self.playing = False
        self.recording = False
        
        self.streamhandler = StreamHandler()

    def createActions(self):
        self.actionConf = QtGui.QAction(u'&Configure', self,
                                                                checkable = False,
                                                                icon =QtGui.QIcon(':/configure.png'),
                                                                )
        self.actionConf.triggered.connect(self.open_configure)

        self.actionPlay = QtGui.QAction(u'Play/Pause', self,
                                                                checkable = True,
                                                                icon =QtGui.QIcon(':/media-playback-start.png'),
                                                                enabled = False,
                                                                )
        self.actionPlay.triggered.connect(self.play_pause)

        self.actionRec = QtGui.QAction(u'&Rec', self,
                                                                checkable = True,
                                                                icon =QtGui.QIcon(':/media-record.png'),
                                                                enabled = False,
                                                                )
        self.actionRec.triggered.connect(self.rec_stop)




    #~ def createMenus(self):
        #~ pass
    
    def createToolBars(self):
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QtCore.QSize(60, 40))
        
        self.toolbar.addAction(self.actionConf, )
        self.toolbar.addAction(self.actionPlay, )
        self.toolbar.addAction(self.actionRec, )


    def closeEvent(self, event):
        if self.recording:
            event.ignore()
        else:
            if self.playing:
                self.play_pause(play = False)
            event.accept()
        

    def open_configure(self):
        pass
        
        for dev in self.devices:
            dev.close()

        

        dev = FakeMultiSignals(streamhandler = self.streamhandler)
        dev.configure( name = 'Test dev',
                                    nb_channel = 3,
                                    sampling_rate =10000.,
                                    buffer_length = 64,
                                    packet_size = 10,
                                    )
        dev.initialize()
        
        self.devices = [ dev]
        
        for dock in self.docks:
            dock.widget().timer.stop()
            self.removeDockWidget(dock)
        
        self.docks = [ ]
        w1 = Oscilloscope(stream = dev.streams[0])
        dock = QtGui.QDockWidget('Oscilloscope')
        dock.setObjectName( 'Oscilloscope' )
        dock.setWidget(w1)
        self.docks.append(dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)            
        
        self.actionPlay.setEnabled(True)
        

    def play_pause(self, play = None):
        
        if play is None:
            self.playing = self.actionPlay.isChecked()
        else:
            self.playing = play
            self.actionPlay.setChecked(play)
        
        print self.playing
        if self.playing:
            # start devices
            self.actionRec.setEnabled(True)
            self.actionConf.setEnabled(False)

            for dev in self.devices:
                dev.start()
            
        else:
            # stop devices
            self.actionRec.setEnabled(False)
            self.actionConf.setEnabled(True)
            
            for dev in self.devices:
                dev.stop()
    

    def rec_stop(self):
        self.recording = self.actionRec.isChecked()
        print self.recording
        if self.recording:
            # start rec
            fd = QtGui.QFileDialog(fileMode= QtGui.QFileDialog.Directory, acceptMode = QtGui.QFileDialog.AcceptSave)
            if fd.exec_():
                
                dirname = unicode(fd.selectedFiles()[0])
                os.mkdir(dirname)
                streams = [ ]
                for dev in self.devices:
                    streams.extend(dev.streams)
                self.rec = RawDataRecording(streams, dirname)
                self.rec.start()
                
                self.actionPlay.setEnabled(False)
            else:
                self.recording = False
                self.recording = self.actionRec.setChecked(False)
                
        else:
            # stop rec
            self.rec.stop()
            self.actionPlay.setEnabled(True)
    
    



def start_mainwindow():
    app = QtGui.QApplication([])
    w = MainWindow()
    w.resize(800, 640)
    w.show()
    
    app.exec_()
    
    
    
if __name__ == '__main__':
    start_mainwindow()
