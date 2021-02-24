#/usr/bin/env python3

# This file contains a set of classes and methods to handle
# running a OPC UA server on a raspberry pi.


import asyncio
import random
from asyncua import ua, uamethod, Server
import announce_service as sa

SERVER_NAME = "RaspPI OPC UA Server"
FLAT_NAME = SERVER_NAME.replace(" ", "")
SERVER_ENDPOINT = "opc.tcp://0.0.0.0:4840"
UA_NAMESPACE = "hvproj:ua:"+FLAT_NAME
TEMP = 19


# This ua method is used to subscribe to a variable on
# another server.
# Inputs:
# endpoint(string): the path to server to subscribe from.
# qx(string): The variable to subscribe to
# ix(string): The variable to connect subscription to
# Returns a Boolean value, depending on if the subscription
# was successful or not.
@uamethod
def subscribe(parent, endpoint, qx, ix):
    client = Client(endpoint)
    try:
        client.connect()
        client.load_type_definitions()

        #root = client.get_root_node()

        #uri = "http://examples.freeopcua.github.io"
        #idx = client.get_namespace_index(uri)

        qxvar = client.get_node(qx)

        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(qxvar)
        time.sleep(0.1)
    except:
        return False

    return True

class SubHandler():
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

client = None
handler = SubHandler()
sub = None
handle = None


class ServerPI:

    def __init__(self):
        self.temp = TEMP
        self.clients = []

    async def go(self):
        server = Server()
        await server.init()
        server.set_endpoint(SERVER_ENDPOINT)
        server.set_server_name(SERVER_NAME)
        server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])

        idx = await server.register_namespace(UA_NAMESPACE)

        dev = await server.nodes.base_object_type.add_object_type(idx, FLAT_NAME)

        lFolder = await server.nodes.objects.add_folder(idx, "Sensors")
        device = await server.nodes.objects.add_object(idx, "ZeDevice", dev)

        zobj = await server.nodes.objects.add_object(idx, "ZeObject")
        zvar = await zobj.add_variable(idx, "qxTemperature", self.temp)

        endp = ua.Argument()
        endp.Name = "Endpoint"
        endp.DataType = ua.NodeId(ua.ObjectIds.String)
        endp.ValueRank = -1
        endp.ArrayDimensions = []
        endp.Description = ua.LocalizedText("Address to endpoint")
        qxvar = ua.Argument()
        qxvar.Name = "qx"
        qxvar.DataType = ua.NodeId(ua.ObjectIds.String)
        qxvar.ValueRank = -1
        qxvar.ArrayDimensions = []
        qxvar.Description = ua.LocalizedText("Output variable to connect to server.")
        ixvar = ua.Argument()
        ixvar.Name = "ix"
        ixvar.DataType = ua.NodeId(ua.ObjectIds.String)
        ixvar.ValueRank = -1
        ixvar.ArrayDimensions = []
        ixvar. Description = ua.LocalizedText("Input variable that is to be connected to.")
        res = ua.Argument()
        res.Name = "Result"
        res.DataType = ua.NodeId(ua.ObjectIds.Boolean)
        res.ValueRank = -1
        res.ArrayDimensions = []
        res.Description = ua.LocalizedText("Result if variable was connected or not.")


        submethod = zobj.add_method(idx, "subscribe", subscribe, [endp, qxvar, ixvar], [res])

        async with server:
            while True:
                await asyncio.sleep(0.1)
                await zvar.write_value(self.temp)
                self.temp = 19 + random.random()


if __name__ == "__main__":
    sa.start_service_announcement()
    sp = ServerPI()
    asyncio.run(sp.go())
