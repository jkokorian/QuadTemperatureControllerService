from PyQt4.QtCore import QThread, pyqtSignal, QObject
import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient
from collections import namedtuple
import time


class TemperatureControllerProxy(object):
    """
    This proxy object is a hardcoded 1-on-1 wrapper of the underlying rpc client
    proxy object. The only reason this is necessary is to have autocomplete on the methods
    """
    def __init__(self,tc_service_endpoint,zmq_context):
        
        rpc_client = RPCClient(
            JSONRPCProtocol(),
            ZmqClientTransport.create(zmq_context, tc_service_endpoint)
        )

        self._remote = rpc_client.get_proxy()
    
    def get_pv(self):
        return self._remote.get_pv()

    def get_working_setpoint(self):
        return self._remote.get_working_setpoint()
    
    def get_setpoint1(self):
        return self._remote.get_setpoint1()
        
    def get_setpoint2(self):
        return self._remote.get_setpoint2()
        
    def set_setpoint1(self, value):
        self._remote.set_setpoint1(value)

    def set_setpoint2(self, value):
        self._remote.set_setpoint2(value)

    def set_remote_setpoint(self,value):
        self._remote.set_remote_setpoint(value)
        
    def get_status(self):
        return self._remote.get_status()
    

class TemperatureControllerUpdater(QThread):
    hardwareStateChanged = pyqtSignal(dict)
    hardwareOutOfSync = pyqtSignal()
    hardwareSynchronized = pyqtSignal()
    
    def __init__(self,tc_service_endpoint, zmq_context):
        QThread.__init__(self)
        
        self.proxy = TemperatureControllerProxy(tc_service_endpoint,zmq_context)
        self.__requested_setpoint1 = None
        self.__requested_setpoint2 = None
        self.__requested_remote_setpoint = None
        
        
    def run(self):
        while True:
            time.sleep(0.05)
            self.__writeRequestedValuesToHardware()
            
            pv = self.proxy.get_pv()
            setpoint1 = self.proxy.get_setpoint1()
            setpoint2 = 0.0
            #setpoint2 = self.proxy.get_setpoint2()
            remote_setpoint = 0.0
            working_setpoint = setpoint1
            status = self.proxy.get_status()
            
            
            state = dict(pv=pv, 
                         setpoint1=setpoint1, 
                         setpoint2=setpoint2, 
                         remote_setpoint=remote_setpoint, 
                         working_setpoint=working_setpoint,
                         status=status)
            self.hardwareStateChanged.emit(state)
        
    def set_setpoint1(self, value):
        self.__requested_setpoint1 = value
        self.hardwareOutOfSync.emit()

    def set_setpoint2(self, value):
        self.__requested_setpoint2 = value
        self.hardwareOutOfSync.emit()

    def set_remote_setpoint(self,value):
        self.__requested_remote_setpoint = value
        self.hardwareOutOfSync.emit()
    
    def __writeRequestedValuesToHardware(self):
        if (self.__requested_setpoint1 is not None):
            self.proxy.set_setpoint1(self.__requested_setpoint1)
            self.__requested_setpoint1 = None
            
        if (self.__requested_setpoint2 is not None):
            self.proxy.set_setpoint2(self.__requested_setpoint2)
            self.__requested_setpoint2 = None
            
        if (self.__requested_remote_setpoint is not None):
            self.proxy.set_remote_setpoint(self.__requested_remote_setpoint)
            self.__requested_remote_setpoint = None
        
        self.hardwareSynchronized.emit()
            

class TemperatureControllerGuiProxy(QObject):
    hardwareStateChanged = pyqtSignal(dict)
    hardwareOutOfSync = pyqtSignal()
    hardwareSynchronized = pyqtSignal()
    
    def __init__(self, tc_service_endpoint, zmq_context):
        self._updater = TemperatureControllerUpdater(tc_service_endpoint,zmq_context)
        self.__hardwareState = dict(pv=0.0, setpoint1=0.0, setpoint2=0.0, remote_setpoint=0.0, working_setpoint=0.0)

        self._updater.hardwareStateChanged.connect(self.__updater_hardwareStateChanged)
        self._updater.hardwareOutOfSync.connect(self.hardwareOutOfSync.emit)
        self._updater.hardwareSynchronized.connect(self.hardwareSynchronized.emit)

        self._updater.start()
    
    def __updater_hardwareStateChanged(self,state):
        self.__hardwareState = state
        self.hardwareStateChanged.emit(self.__hardwareState.copy())
    
    @property
    def pv(self):
        return self.__pv
        
    @property
    def setpoint1(self):
        return self.__setpoint1
        
    @property
    def setpoint2(self):
        return self.__setpoint2
        
    @property
    def remote_setpoint(self):
        return self.__remote_setpoint
        
    @property
    def working_setpoint(self):
        return self.__working_setpoint
    
    @property
    def status(self):
        self.__status
    
    def set_setpoint1(self,value):
        self._updater.set_setpoint1(value)
        
    def set_setpoint2(self,value):
        self._updater.set_setpoint2(value)
        
    def set_remote_setpoint(self,value):
        self._updater.set_remote_setpoint(value)
        
    
    

        
        
        
        
        
        
        
        
        
        
        
    