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
        self.qxBall = True
        self.qxBarrel = True
        self.clients = {}
    
    # This ua method is used to subscribe to a variable on
    # another server.
    # Inputs:
    # endpoint(Server url as string): the path to server to subscribe from.
    # qx(NodeId in string format): The variable to subscribe to
    # ix(NodeId in string fromat): The variable to connect subscription to
    # Returns void.
    @uamethod
    async def subscribe(self, parent, endpoint, qx, ix):
        server = str(endpoint)
        if server not in self.clients:
            try:
                client = Client(server)
                await client.connect()
                await client.load_data_type_definitions()
                self.clients[server] = (client,set())
            except:
                return "Could not reach the server specified."
        else:
            client = self.clients[server][0]

        #root = client.get_root_node(
        #uri = "http://examples.freeopcua.github.io"
        #idx = client.get_namespace_index(uri)

        qxvar = client.get_node(qx)
        if qx not in self.clients[server][1]:
            self.clients[server][1].add(qx)
            print(len(self.clients[server][1]))
            sub = await client.create_subscription(500, handler)
            handle = await sub.subscribe_data_change(qxvar)
        time.sleep(0.1)
        return "Successfully subscribed to the specified variable!"
            
    def method_var(self, name, description):
        arg = ua.Argument()
        arg.Name = name
        arg.DataType = ua.NodeId(ua.ObjectIds.Int64) #NodeId, and not datatype of value. We use Int64 ID's.
        arg.ValueRank = -1
        arg.ArrayDimensions = []
        arg.Description = ua.LocalizedText(description)
        return arg

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
        print("Sensors folder: ", lFolder)
        zobj = await objects.add_object(idx, "Methods")
        print("Methods object:", zobj)

        xvar = await lFolder.add_variable(idx, "qxBarrel", self.qxBarrel)
        yvar = await lFolder.add_variable(idx, "qxBall", self.qxBall)
        zvar = await lFolder.add_variable(idx, "qxTemperature", self.temp)
        print("Temp var: ", zvar)
        print("qxBall var:", yvar)
        print("qxBarrel var:", xvar)

        endp = self.method_var("Endpoint", "Address to tendpoint")
        qxvar = self.method_var("qx", "Output variable to connect to server.")
        ixvar = self.method_var("ix", "Input variable that is to be connected to.")
        ret = self.method_var("ret", "Return message for information of what happend.")

        await zobj.add_method(idx, "subscribe", self.subscribe, [endp, qxvar, ixvar], [ret])

        async with server:
            while True:
                await asyncio.sleep(1.2)
                await zvar.write_value(self.temp)
                await yvar.write_value(self.qxBall)
                await xvar.write_value(self.qxBarrel)
                self.temp = 19 + random.random()
                self.qxBall = not self.qxBall
                self.qxBarrel = not self.qxBarrel
                print(self.temp)
                print(self.qxBall)
                print(self.qxBarrel)


if __name__ == "__main__":
    print(DISCOVERY_NAME)
    sa.start_service_announcement(device_name=DISCOVERY_NAME, iport=SERVER_PORT)
    sp = ServerPI()
    asyncio.run(sp.go())
