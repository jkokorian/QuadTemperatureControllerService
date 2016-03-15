import serial
from hardware import QuadTemperatureController
import argparse
import zmq

from tinyrpc.transports.zmq import ZmqServerTransport
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.dispatch import RPCDispatcher,public

from tinyrpc.server import RPCServer

from os import system


def portNameToInt(portName):
    if (portName.startswith("COM") and len(portName) > 3):
        return int(portName[3:])-1


if __name__=="__main__":
    
    system("Title "+ "Device Service: Quad Temperature Controller")    

    parser = argparse.ArgumentParser(description="Device service for the Kokorian Valve & Flow System Controller")
    parser.add_argument("--device-port","-d",dest="serialPortName",type=str,default="COM5")
    parser.add_argument("--baud-rate","-b",dest="baudrate",type=int,default=9600)
    parser.add_argument("--service-port","-p",dest="servicePort",type=int,default=5060)
    parser.add_argument("--service-ip",dest="serviceIP",type=str,default="127.0.0.1")
    
    args = parser.parse_args()
        
    qtc = QuadTemperatureController(args.serialPortName,args.baudrate)
    
    dispatcher = RPCDispatcher()
    dispatcher.register_instance(qtc)
    
    ctx = zmq.Context()
    
    endpoint = 'tcp://%s:%i' % (args.serviceIP,args.servicePort)
    transport = ZmqServerTransport.create(ctx, endpoint)
    print "serving requests at %s" % endpoint
    
    
    rpc_server = RPCServer(
        transport,
        JSONRPCProtocol(),
        dispatcher
    )
    
    rpc_server.serve_forever()