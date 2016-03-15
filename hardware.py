from tinyrpc.dispatch import public
from eurotherm3216 import Eurotherm3216

class QuadTemperatureController(object):
    def __init__(self,portname,baudrate):
        self.tc1 = Eurotherm3216(portname,1, baudrate)
        self.tc2 = Eurotherm3216(portname,2, baudrate)
        self.tc3 = Eurotherm3216(portname,3, baudrate)
        self.tc4 = Eurotherm3216(portname,4, baudrate)

        self._tcDict = {}
        for name in "tc1 tc2 tc3 tc4".split(' '):
            self._tcDict[name] = getattr(self,name)
            
        

    @public
    def get_temperature_controller_state(self, name):
        tc = self._tcDict[name]
        return dict(process_temperature=tc.get_pv(),
                    working_setpoint=tc.get_working_setpoint(),
                    setpoint1=tc.get_setpoint1())
        

    
