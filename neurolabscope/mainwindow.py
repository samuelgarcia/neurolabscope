# -*- coding: utf-8 -*-
"""
Neurolabscope mainwindow.
"""

from PyQt4 import QtCore,QtGui
import os
from collections import OrderedDict
import json
import copy
import datetime


from pyacq import StreamHandler, FakeMultiSignals, RawDataRecording, device_classes
from pyacq.gui import Oscilloscope

dict_device_classes = OrderedDict()
for c in device_classes:
    dict_device_classes[c.__name__] = c

from .guiutil import icons, PickleSettings

from .views import views_dict
from .configure import ConfigWindow
from .metadatatool import MetadataWidget
from .recordinglist import RecordingList
from .version import version
from .default_setup import default_setup

applicationname = 'Neurolabscope 0.2'

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent  = None, setup = None):
        QtGui.QMainWindow.__init__(self, parent = parent)
        
        self.settings = PickleSettings(applicationname=applicationname)
        if setup is None:
            setup = default_setup
            
            filename = self.settings['last_setup_filname']
            #~ print filename
            if filename is not None and os.path.exists(filename):
                try:
                    setup = json.load(open(filename))
                except:
                    self.warning_setup(filename)
                    
        
        
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
        
        # patch options in setup in case of seomthing new:
        d = setup['options']
        setup['options'] = copy.deepcopy(default_setup['options'])
        setup['options'].update(d)
        
        
        #~ self.apply_setup(setup)
        try:
            self.apply_setup(setup)
        except:
            self.warning_setup(filename)
            setup = default_setup
            self.apply_setup(setup)
            

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
        self.actionRec.triggered.connect(self.on_rec_button_pushed)




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
    
    def warning_setup(self, filename = None):
        text = u'Setup file contains errors.'
        if filename is not None:
            text += ' ({})'.format(filename)
        mb = QtGui.QMessageBox.warning(self, u'Setup file problem',text, 
                QtGui.QMessageBox.Ok ,  QtGui.QMessageBox.Default  | QtGui.QMessageBox.Escape,
                QtGui.QMessageBox.NoButton)
        
    
    def apply_setup(self, setup):
        # close old one
        for dev in self.devices:
            dev.close()
        for dock in self.docks:
            if hasattr(dock.widget(), 'timer'):
                dock.widget().timer.stop()
            self.removeDockWidget(dock)
        
        # Devices
        self.devices = [ ]
        for dev_info in setup['devices']:
            _class = dict_device_classes[dev_info['class']]
            dev = _class(streamhandler = self.streamhandler)
            dev.configure(subdevices = dev_info['subdevices'],
                                **dev_info['global_params'])
            dev.initialize()
            self.devices.append(dev)
        
        # Views
        self.docks = [ ]
        for view in setup['views']:
            _class = views_dict[view['class']]
            widget = _class(stream = self.devices[view['device_num']].streams[view['subdevice_num']])
            widget.set_params(**view['params'])
            dock = QtGui.QDockWidget(view['name'])
            dock.setWidget(widget)
            self.docks.append(dock)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        
        
        self.actionPlay.setEnabled(True)
        
        # Global options
        self.setup = setup
        
        # consistency
        if self.setup['options']['filename_mode'] == 'Generate with metadata':
            self.setup['options']['show_metadata_tool'] = True
        
        if self.setup['options']['show_metadata_tool']:
            param_metadata = self.setup.get('param_metadata', None)
            self.metadata_widget = MetadataWidget(param_metadata = param_metadata)
            dock = QtGui.QDockWidget('Metadata')
            dock.setWidget(self.metadata_widget)
            self.docks.append(dock)
            self.dock_metadata = dock
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            self.metadata_widget.setMaximumWidth(250) # FIXME : do better
        else:
            self.dock_metadata = None
            self.metadata_widget= None
            
            
        if self.setup['options']['show_file_list']:
            self.reclist_widget = RecordingList()
            dock = QtGui.QDockWidget('RecordingList')
            dock.setWidget(self.reclist_widget)
            self.docks.append(dock)
            self.dock_reclist = dock
            #~ self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        
        p = self.setup['options']['recording_directory']
        QtCore.QDir(p).mkpath(p)
        
        

    def save_setup(self, filename):
        if self.setup['options']['show_metadata_tool']:
            self.setup['param_metadata'] = self.metadata_widget.get_param_metadata()
        
        for i, view in enumerate(self.setup['views']):
            
            view['params'] = self.docks[i].widget().get_params()
        
        json.dump(self.setup,open(filename, 'wb'), indent=4, separators=(',', ': '))
        
        

    def open_configure(self):
        w = ConfigWindow(parent = self, setup = self.setup)
        if w.exec_():
            self.apply_setup(w.get_setup())
            if w.setup_filename is not None:
                self.settings['last_setup_filname'] = w.setup_filename


    def play_pause(self, play = None):
        
        if play is None:
            self.playing = self.actionPlay.isChecked()
        else:
            self.playing = play
            self.actionPlay.setChecked(play)
        
        
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

    def get_new_dirname(self, now = None):
        basename = self.setup['options']['recording_directory']
        
        if self.setup['options']['filename_mode'] == 'Ask on record':
            fd = QtGui.QFileDialog(  fileMode= QtGui.QFileDialog.AnyFile,
                                                        acceptMode = QtGui.QFileDialog.AcceptSave,
                                                        options = QtGui.QFileDialog.ShowDirsOnly)
            fd.setDirectory(QtCore.QString(basename))
            if fd.exec_():
                dirname = unicode(fd.selectedFiles()[0])
                os.mkdir(dirname)
            else:
                dirname = None
        
        elif self.setup['options']['filename_mode'] == 'Generate with metadata':
            name = now.strftime('%Y-%m-%d-%Hh%Mm%S,%fs')
            name = name +'_'+ '_'.join([ '{}={}'.format(k,v) for k, v in self.metadata_widget.get_metadata().items()])
            dirname = os.path.join(basename, name)
            os.mkdir(dirname)
        
        return dirname
    
    def start_rec(self, dirname, now):
        assert self.recording==False
        streams = [ ]
        for dev in self.devices:
            streams.extend(dev.streams)
        self.rec_engine = RawDataRecording(streams, dirname)
        self.rec_engine.start()
        self.actionPlay.setEnabled(False)
        self.recording = True
        
        if self.setup['options']['show_file_list']:
            name = os.path.basename(dirname)
            self.reclist_widget.add_rec(name, dirname, now, state = 'recording')
    
    def stop_rec(self):
        assert self.recording==True
        self.rec_engine.stop()
        self.actionPlay.setEnabled(True)
        self.recording = False

        if self.setup['options']['show_file_list']:
            self.reclist_widget.list[-1]['state'] = 'finished'
        
    
    def on_rec_button_pushed(self):
        
        if self.actionRec.isChecked():
            now = datetime.datetime.now()
            # enable or start rec
            if self.setup['options']['recording_mode'] == 'continuous':
                dirname = self.get_new_dirname(now = now)
                #~ print dirname
                if dirname is None:
                    self.actionRec.setChecked(False)
                    return
                else:
                    self.start_rec(dirname, now)
            else:
                pass
            
        else:
            # disable or stop rec
            if self.setup['options']['recording_mode'] == 'continuous':
                self.stop_rec()
            else:
                pass
    
    
    def closeEvent (self, event):
        if self.playing:
            event.ignore()
        else:
            if self.setup['options']['auto_save_setup_on_exit']:
                self.save_setup(self.settings['last_setup_filname'])
            event.accept()
    

        
        



def start_mainwindow():
    app = QtGui.QApplication([])
    w = MainWindow()
    w.resize(800, 640)
    w.show()
    
    app.exec_()
    
    
    
if __name__ == '__main__':
    start_mainwindow()
