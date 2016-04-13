from tinyrpc.dispatch import public
from hardware import Eurotherm3216, Eurotherm3216Spoof
import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient



class QuadTemperatureController(object):
    def __init__(self,portname,baudrate,fake=False):

        ET3216 = Eurotherm3216 if not fake else Eurotherm3216Spoof       
        
        self.tc1 = ET3216(portname,1, baudrate)
        self.tc2 = ET3216(portname,2, baudrate)
        self.tc3 = ET3216(portname,3, baudrate)
        self.tc4 = ET3216(portname,4, baudrate)
    

        self._tcDict = {}
        for name in "tc1 tc2 tc3 tc4".split(' '):
            self._tcDict[name] = getattr(self,name)
    
    @public
    def get_temperature_controller_state(self, name):
        tc = self._tcDict[name]
        return dict(process_temperature=tc.get_pv(),
                    working_setpoint=tc.get_working_setpoint(),
                    setpoint1=tc.get_setpoint1())
    
    @public    
    def get_pv(self, device_id):
        return self._tcDict[device_id].get_pv();

    @public
    def get_working_setpoint(self, device_id):
        return self._tcDict[device_id].get_working_setpoint()

    @public
    def get_setpoint1(self, device_id):
        return self._tcDict[device_id].get_setpoint1()
        
    @public
    def get_setpoint(self, device_id):
        return self._tcDict[device_id].get_setpoint2()

    @public
    def set_setpoint1(self, device_id, value):
        return self._tcDict[device_id].set_setpoint1(value)

    @public
    def set_setpoint2(self, device_id, value):
        return self._tcDict[device_id].set_setpoint2(value)

    @public
    def set_remote_setpoint(self, device_id, value):
        return self._tcDict[device_id].set_remote_setpoint(value)

    @public
    def get_status(self, device_id):
        return self._tcDict[device_id].get_status()

    
class TemperatureControllerService(object):
    
    def __init__(self, modbus_service_endpoint, device_id, zmq_context=None):
        self.device_id = device_id
        if zmq_context is None:
            self.zmq_context = zmq.Context()
        else:
            self.zmq_context = zmq_context
        self._rpc_client = RPCClient(
            JSONRPCProtocol(),
            ZmqClientTransport.create(self.zmq_context, modbus_service_endpoint)
        )
        self.modbus_proxy = self._rpc_client.get_proxy()
    
    @public    
    def get_pv(self):
        return self.modbus_proxy.get_pv(self.device_id);

    @public
    def get_working_setpoint(self):
        return self.modbus_proxy.get_working_setpoint(self.device_id);

    @public
    def get_setpoint1(self):
        return self.modbus_proxy.get_setpoint1(self.device_id);
        
    @public
    def get_setpoint2(self):
        return self.modbus_proxy.get_setpoint2(self.device_id)
    
    @public
    def set_setpoint1(self, value):
        return self.modbus_proxy.set_setpoint1(self.device_id, value);

    @public
    def set_setpoint2(self, value):
        return self.modbus_proxy.set_setpoint2(self.device_id, value);

    @public
    def set_remote_setpoint(self,value):
        return self.modbus_proxy.set_remote_setpoint(self.device_id, value);
        
    @public
    def get_status(self):
        return self.modbus_proxy.get_status(self.device_id)