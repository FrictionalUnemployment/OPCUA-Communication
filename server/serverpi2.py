#/usr/bin/env python3

# This file contains a set of classes and methods to handle
# running a OPC UA server on a raspberry pi.


import asyncio
import random
import time
from asyncua import ua, uamethod, Server, Client
import announce_service as sa

SERVER_NAME = "2RaspPI OPC UA Server"
FLAT_NAME = SERVER_NAME.replace(" ", "")
SERVER_PORT = 4841
SERVER_ENDPOINT = "opc.tcp://0.0.0.0:"+str(SERVER_PORT)
UA_NAMESPACE = "hvproj:ua:"+FLAT_NAME
DISCOVERY_NAME="_"+FLAT_NAME[:10]+"."
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
    print("Inside subscribe!")
    client = Client(endpoint.Value)
    try:
        print("Try to connect")
        client.connect()
        client.load_type_definitions()
        print("Before get node")

        #root = client.get_root_node()

        #uri = "http://examples.freeopcua.github.io"
        #idx = client.get_namespace_index(uri)

        qxvar = client.get_node(qx)
        print("After get node")

        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(qxvar)
        time.sleep(0.1)
    except:
        pass

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
        #server.set_security_policy([
        #    ua.SecurityPolicyType.NoSecurity,
        #    ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        #    ua.SecurityPolicyType.Basic256Sha256_Sign])

        idx = await server.register_namespace(UA_NAMESPACE)

        objects = server.nodes.objects

        #dev = await server.nodes.base_object_type.add_object_type(idx, FLAT_NAME)

        lFolder = await objects.add_folder(idx, "Sensors")
        zobj = await objects.add_object(idx, "Methods")

        zvar = await lFolder.add_variable(idx, "ixTemperature", self.temp)

        endp = ua.Argument()
        endp.Name = "Endpoint"
        endp.DataType = ua.NodeId(ua.ObjectIds.Int64) #NodeId, and not datatype of value. We use Int64 ID's.
        endp.ValueRank = -1
        endp.ArrayDimensions = []
        endp.Description = ua.LocalizedText("Address to endpoint")
        qxvar = ua.Argument()
        qxvar.Name = "qx"
        qxvar.DataType = ua.NodeId(ua.ObjectIds.Int64) #NodeId, and not datatype of value. We use Int64 ID's.
        qxvar.ValueRank = -1
        qxvar.ArrayDimensions = []
        qxvar.Description = ua.LocalizedText("Output variable to connect to server.")
        ixvar = ua.Argument()
        ixvar.Name = "ix"
        ixvar.DataType = ua.NodeId(ua.ObjectIds.Int64) #NodeId, and not datatype of value. We use Int64 ID's.
        ixvar.ValueRank = -1
        ixvar.ArrayDimensions = []
        ixvar. Description = ua.LocalizedText("Input variable that is to be connected to.")
        res = ua.Argument()
        res.Name = "Result"
        res.DataType = ua.NodeId(ua.ObjectIds.Int64) #NodeId, and not datatype of value. We use Int64 ID's.
        res.ValueRank = -1
        res.ArrayDimensions = []
        res.Description = ua.LocalizedText("Result if variable was connected or not.")

        await zobj.add_method(idx, "subscribe", subscribe, [endp, qxvar, ixvar], [])

        async with server:
            while True:
                await asyncio.sleep(2)
                await zvar.write_value(self.temp)
                self.temp = 19 + random.random()
                print(self.temp)


if __name__ == "__main__":
    print(DISCOVERY_NAME)
    sa.start_service_announcement(device_name=DISCOVERY_NAME, iport=SERVER_PORT)
    sp = ServerPI()
    asyncio.run(sp.go())
