#usr/bin/env python3

# This file contains a set of classes and methods to handle
# running a OPC UA server on a raspberry pi.


import asyncio
import random
import time
from asyncua import ua, uamethod, Server, Client
import announce_service as sa

SERVER_NAME = "RaspPI OPC UA Server"
FLAT_NAME = SERVER_NAME.replace(" ", "")
SERVER_PORT = 4840
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
    def __init__(self, variables, client, localserver):
        self.vars = variables
        self.cl = client
        self.srv = localserver

    async def datachange_notification(self, node, val, data):
        n = self.srv.get_node(self.vars[str(node)])
        await n.write_value(val)
        print(self.vars)
        print("Python: New data change event", n, val)

    def event_notification(self, event):
        print("Python: New event", event)

class ServerPI:

    def __init__(self):
        self.server = None
        self.temp = TEMP
        self.ixBall = False
        self.ixBarrel = False
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
        # The client tuple consists of a Client object, a SubHandler object,
        # a Subscription, a list of subscribed variables, and a dictionary of 
        # subscribed and connected variables as strings.
        server = str(endpoint)
        if server not in self.clients.keys():
            try:
                client = Client(server)
                print("After Client(server)")
                await client.connect()
                print("After client.connect()")
                await client.load_data_type_definitions()
                print("After client.loaddatattype")
                tmpvariables = {}
                tmphandler = SubHandler(tmpvariables, client, self.server)
                tmpsubscription = await client.create_subscription(500, tmphandler)
                self.clients[server] = (client, tmphandler, tmpsubscription, [], tmpvariables)
            except:
                return "Could not reach the server specified."
        else:
            client = self.clients[server][0]

        qxvar = client.get_node(qx)
        if qx not in self.clients[server][4].keys():
            self.clients[server][4][qx] = ix
            subbedvar = await self.clients[server][2].subscribe_data_change(qxvar)
            self.clients[server][3].append(subbedvar)
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
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(SERVER_ENDPOINT)
        self.server.set_server_name(SERVER_NAME)
        #server.set_security_policy([
        #    ua.SecurityPolicyType.NoSecurity,
        #    ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        #    ua.SecurityPolicyType.Basic256Sha256_Sign])

        idx = await self.server.register_namespace(UA_NAMESPACE)

        objects = self.server.nodes.objects

        lFolder = await objects.add_folder(idx, "Sensors")
        zobj = await objects.add_object(idx, "Methods")
        zvar = await lFolder.add_variable(idx, "ixTemperature", self.temp)
        yvar = await lFolder.add_variable(idx, "ixBall", self.ixBall)
        xvar = await lFolder.add_variable(idx, "ixBarrel", self.ixBarrel)
        yvar.set_writable()
        xvar.set_writable()
        zvar.set_writable()
        print(zvar)
        print(yvar)
        print(xvar)

        endp = self.method_var("Endpoint", "Address to tendpoint")
        qxvar = self.method_var("qx", "Output variable to connect to server.")
        ixvar = self.method_var("ix", "Input variable that is to be connected to.")
        ret = self.method_var("ret", "Return message for information of what happend.")
        await zobj.add_method(idx, "subscribe", self.subscribe, [endp, qxvar, ixvar], [ret])

        async with self.server:
            while True:
                await asyncio.sleep(0.1)

if __name__ == "__main__":
    print(DISCOVERY_NAME)
    sa.start_service_announcement(device_name=DISCOVERY_NAME, iport=SERVER_PORT)
    sp = ServerPI()
    asyncio.run(sp.go())
