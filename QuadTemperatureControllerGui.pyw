# -*- coding: utf-8 -*-
"""
Created on Tue Apr 07 12:24:22 2015

@author: ODMS-admin
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from proxies import TemperatureControllerUpdater
import pyqtgraph as pg
import sys
import zmq

import time
import numpy as np




class EnterKeySpinbox(pg.SpinBox):
    enterKeyPressed = pyqtSignal()
    delayedFocusLost = pyqtSignal()
    
    def __init__(self, parent=None,value=0.0, **kwargs):
        pg.SpinBox.__init__(self,parent=parent, value=value, **kwargs)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return: 
            self.enterKeyPressed.emit()
        pg.SpinBox.keyPressEvent(self, event)
        
    def focusOutEvent(self, event):
        pg.SpinBox.focusOutEvent(self, event)
        QTimer.singleShot(1000,lambda: self.delayedFocusLost.emit())
        

class SetpointEditor(QWidget):
    setpointChangeRequested = pyqtSignal(float)

    def __init__(self, setpoint_name, parent=None, **pg_spinbox_kwargs):
        QWidget.__init__(self,parent)

        #create widgets
        self.setpointName = setpoint_name
        self.setpointLabel = QLabel(setpoint_name,parent=self)
        self.spinbox = EnterKeySpinbox(parent=self, **pg_spinbox_kwargs)
        self.spinbox.setKeyboardTracking(False)
        self.setButton = QToolButton()
        self.setButton.setText("set")
        
        #create properties
        self.__actualSetpoint = 0.0
        self.__requestedSetpoint = 0.0

        #create layout

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.spinbox)        
        hlayout.addWidget(self.setButton)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.setpointLabel)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

        #register signals
        self.setButton.clicked.connect(self._setpointChanging)
        self.spinbox.delayedFocusLost.connect(self._setpointChanging)
        self.spinbox.enterKeyPressed.connect(self._setpointChanging)

        self.initializeValues()

    def initializeValues(self):
        pass
        

    def _revertRequestedSetpoint(self):
        self.spinbox.setValue(self.getRequestedSetpoint())

    
    def setActualSetpoint(self,value):
        if value != self.getActualSetpoint():
            self.__actualSetpoint = value
            
        self.setpointLabel.setText("%s: <b>%0.1f</b>" % (self.setpointName, value))
        
    
    def getActualSetpoint(self):
        return self.__actualSetpoint
        
    def _setpointChanging(self):
        self._setRequestedSetpoint(self.spinbox.value())
    
    def _setRequestedSetpoint(self,value):
        self.__requestedSetpoint = value
        #self._updateBackgroundColor()
        self.setpointChangeRequested.emit(value)
        print "setpoint change requested", value
        
    def getRequestedSetpoint(self):
        return self.__requestedSetpoint
    
        
    
    def _updateBackgroundColor(self):
        palette = QPalette();
        if (self.isSynchronized):
            palette.setColor(QPalette.Base,Qt.green);
        else:
            palette.setColor(QPalette.Base,Qt.red);
            
        self.spinbox.setPalette(palette);


    @property
    def isSynchronized(self):
        """
        Gets whether the hardware setpoint matches the requested setpoint
        """
        return self.getHardwareSetpoint() == self.getRequestedSetpoint()



class FakeTCUpdateThread(QThread):
    hardwareStateChanged = pyqtSignal(dict)
    def run(self):
        while True:
            time.sleep(0.1)
            state = {'pv': np.random.rand()*10, 
                     'setpoint1': np.random.rand()*10}
            
            self.hardwareStateChanged.emit(state)
            



class TemperatureControllerWidget(QGroupBox):
    def __init__(self, updater, name="TemperatureController", parent=None):
        QWidget.__init__(self,title=name, parent=parent)
        
        self.name = name
        layout = QVBoxLayout()
        self.actualTemperatureDisplay = QLabel(parent=self)
        self.setpointEditor = SetpointEditor("Setpoint",suffix=u'°C', siPrefix=True, dec=True, step=0.1, minStep=0.1)
        layout.addWidget(self.actualTemperatureDisplay)
        layout.addWidget(self.setpointEditor)

        self.setLayout(layout)
        
        self.hardwareProxy = updater
        
        #connect signals and slots
        self.hardwareProxy.hardwareStateChanged.connect(self.hardwareThread_hardwareStateChanged)
        self.setpointEditor.setpointChangeRequested.connect(self.hardwareProxy.set_setpoint1)
        
        self.initialize()
        
    def initialize(self):
        self.updateActualTemperature(0.0)
        self.hardwareProxy.start()
        
        
    def updateActualTemperature(self,value):
        self.actualTemperatureDisplay.setText(u"process temperature: <b>%0.1f °C</b>" % value)
        
    def updateActualSetpoint(self,value):
        self.setpointEditor.setActualSetpoint(value)
        
    def hardwareThread_hardwareStateChanged(self,state):
        self.updateActualTemperature(state['pv'])
        self.updateActualSetpoint(state['setpoint1'])
        

    def closeEvent(self, event):
        # do stuff
        self.hardwareThread.terminate()
        event.accept()

                
            

class QuadTemperatureControllerWidget(QWidget):
    def __init__(self,parent=None):
        super(QuadTemperatureControllerWidget,self).__init__()
        layout = QHBoxLayout()
        
        ctx = zmq.Context()
        
        self.tcBubberWidget = TemperatureControllerWidget(name="Bubbler Temperature Controller", updater=TemperatureControllerUpdater("tcp://127.0.0.1:5061", ctx))
        self.tcGasWidget = TemperatureControllerWidget(name="Gas Temperature Controller", updater=TemperatureControllerUpdater("tcp://127.0.0.1:5062", ctx))
        self.tcChamberBaseWidget = TemperatureControllerWidget(name="Chamber Base Temperature Controller", updater=TemperatureControllerUpdater("tcp://127.0.0.1:5063", ctx))
        self.tcChamberWallWidget = TemperatureControllerWidget(name="Chamber Wall Temperature Controller", updater=TemperatureControllerUpdater("tcp://127.0.0.1:5064", ctx))
        
        
        for w in [self.tcBubberWidget, self.tcGasWidget, self.tcChamberWallWidget, self.tcChamberBaseWidget]:
            layout.addWidget(w)

        self.setLayout(layout)

        
    def closeEvent(self, event):
        # do stuff
        event.accept()


def main():
    
    app= QApplication(sys.argv)
    widget = QuadTemperatureControllerWidget()
    widget.setWindowTitle("Quad Temperature Controller Unit")
    widget.setWindowFlags(Qt.WindowStaysOnTopHint)
    widget.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()
    