#!/usr/bin/env python
#
#   Copyright 2012 Jonas Berg
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""

.. moduleauthor:: Jonas Berg <pyhys@users.sourceforge.net>

Driver for the Eurotherm3500 process controller, for communication via the Modbus RTU protocol.

"""

import minimalmodbus


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
    
