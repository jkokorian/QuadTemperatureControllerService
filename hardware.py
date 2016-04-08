

import minimalmodbus

import numpy as np


class Eurotherm3216Spoof():
    def __init__(self,*args,**kwargs):
        self.working_setpoint = 10
        self.setpoint1 = 0
        self.setpoint2 = 0
        self.remote_setpoint = 0
        
    def get_pv(self):
        return self.setpoint1 + np.random.rand()*0.3

    def get_working_setpoint(self):
        return self.setpoint1
    
    def get_setpoint1(self):
        return self.setpoint1
        
    def get_setpoint2(self):
        return self.setpoint2
        
    def set_setpoint1(self, value):
        self.setpoint1 = value

    def set_setpoint2(self, value):
        self.setpoint2 = value

    def set_remote_setpoint(self,value):
        self.remote_setpoint = value


class Eurotherm3216(minimalmodbus.Instrument):
    """Instrument class for Eurotherm 3216 temperature controller. 
    
    Communicates via Modbus RTU protocol (via RS232 or RS485), using the *MinimalModbus* Python module.    

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    Implemented with these function codes (in decimal):
        
    ==================  ====================
    Description         Modbus function code
    ==================  ====================
    Read registers      3
    Write registers     16
    ==================  ====================

    """
    
    def __init__(self, portname, slaveaddress, baudrate):
        minimalmodbus.BAUDRATE = baudrate
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        
    
    ## Process value
    
    def get_pv(self):
        return self.read_register(1,1)

    def get_working_setpoint(self):
        return self.read_register(5,1)
    
    def get_setpoint1(self):
        return self.read_register(24,1)
        
    def set_setpoint1(self, value):
        self.write_register(24,value,numberOfDecimals=1)

    def set_setpoint2(self, value):
        self.write_register(25,value,numberOfDecimals=1)

    def set_remote_setpoint(self,value):
        self.write_register(26,value)
    
