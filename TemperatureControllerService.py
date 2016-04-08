import serial
from hardwareServices import TemperatureControllerService
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
    
    system("Title "+ "Device Service: Temperature Controller")    

    parser = argparse.ArgumentParser(description="Temperature controller unit")
    parser.add_argument("--modbus-service",dest="modbusService",type=str)
    parser.add_argument("--device-id",dest="deviceId",type=str)
    parser.add_argument("--service-port","-p",dest="servicePort",type=int,default=5070)
    parser.add_argument("--service-ip",dest="serviceIP",type=str,default="127.0.0.1")
    
    args = parser.parse_args()
        
    ctx = zmq.Context()
    tcService = TemperatureControllerService(args.modbusService, args.deviceId, ctx)
    
    dispatcher = RPCDispatcher()
    dispatcher.register_instance(tcService)
    
    endpoint = 'tcp://%s:%i' % (args.serviceIP,args.servicePort)
    transport = ZmqServerTransport.create(ctx, endpoint)
    print "serving requests at %s" % endpoint
    
    
    rpc_server = RPCServer(
        transport,
        JSONRPCProtocol(),
        dispatcher
    )
    
    rpc_server.serve_forever()