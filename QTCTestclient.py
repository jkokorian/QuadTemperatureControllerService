import zmq
import time
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient

ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:5060')
)


remote_server = rpc_client.get_proxy()

for i in range(1000):
    for tc in ["tc" + str(i) for i in [1,2,3,4]]:
        print remote_server.get_temperature_controller_state(tc)
