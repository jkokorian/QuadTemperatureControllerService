# -*- coding: utf-8 -*-
"""
Created on Tue Apr 07 12:24:22 2015

@author: ODMS-admin
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import zmq

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient


class Eurotherm3216Widget(QWidget):
	def __init__(self,name="Eurotherm3216", parent=None):
		QWidget.__init__(self,parent)
		
		self.name = name
		layout = QHBoxLayout()
		self.actualTemperatureDisplay = QLabel(parent=self)
		layout.addWidget(self.actualTemperatureDisplay)
		self.setLayout(layout)
		
		
	def updateActualTemperature(self,value):
		self.actualTemperatureDisplay.setText(str(value))
	

class QuadTemperatureControllerWidget(QWidget):
    def __init__(self,parent=None):
        super(QuadTemperatureControllerWidget,self).__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        #self.setWindowTitle("Eurotherm3216")
        
        self.ctx = zmq.Context()

        self.rpc_client = RPCClient(
            JSONRPCProtocol(),
            ZmqClientTransport.create(self.ctx, 'tcp://127.0.0.1:6002')
        )
        
        self.remote_server = self.rpc_client.get_proxy()
        
        self.offButton.clicked.connect(self.offButton_clicked)
        self.onButton.clicked.connect(self.onButton_clicked)
    
        
    def closeEvent(self, event):
        # do stuff
        self.ctx.close()
        event.accept()


        
    
def main():
    
    app= QApplication(sys.argv)
    widget = Eurotherm3216Widget()
    widget.setWindowTitle("Quad Temperature Controller Unit")
    widget.setWindowFlags(Qt.WindowStaysOnTopHint)
    widget.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()
    