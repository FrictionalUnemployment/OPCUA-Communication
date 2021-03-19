#/usr/bin/env python3

# This file contains a set of classes and methods to handle
# running a OPC UA server on a raspberry pi.


import asyncio
import random
import time
from asyncua import ua, uamethod, Server, Client
import announce_service as sa

SERVER_NAME = "OPC UA Server"
FLAT_NAME = SERVER_NAME.replace(" ", "")
SERVER_PORT = 4840
SERVER_ENDPOINT = "opc.tcp://0.0.0.0:"
UA_NAMESPACE = "hvproj:ua:"
DISCOVERY_NAME="_"+FLAT_NAME[:10]+"."

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

    def datachange_notification(self, node, val, data):
        n = self.srv.get_node(self.vars[str(node)])
        n.write_value(val)
        print("Python: New data change event", n, val)

    def event_notification(self, event):
        print("Python: New event", event)

class ServerPI:

    def __init__(self, name=SERVER_NAME, port=SERVER_PORT):
        self.server_name = name
        self.flat_name = name.replace(" ", "")
        self.server = None
        self.server_port = port
        self.ua_namespace = UA_NAMESPACE+self.flat_name
        self.discovery_name = "_"+self.flat_name[:10]+"."
        self.varfolder = None
        self.idx = None
        self.objects = None
        self.clients = {}
        self.localvars = {}
        self.callback_func = None
        self.callback_vars = None

    async def init_server(self):
        print("Inside init_server")
        sa.start_service_announcement(device_name=self.discovery_name, iport=self.server_port)
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(SERVER_ENDPOINT+str(self.server_port))
        self.server.set_server_name(self.server_name)
        #server.set_security_policy([
        #    ua.SecurityPolicyType.NoSecurity,
        #    ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        #    ua.SecurityPolicyType.Basic256Sha256_Sign])

        self.idx = await self.server.register_namespace(self.ua_namespace)
        self.objects = self.server.nodes.objects
        self.varfolder = await self.objects.add_folder(self.idx, "Variables")
        print(type(self.varfolder))
        await self.setup_sub_method()
    
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

    # Helper method for setting up a UA Argument, in this case
    # for use in the subscription method.        
    def method_var(self, name, description):
        arg = ua.Argument()
        arg.Name = name
        arg.DataType = ua.NodeId(ua.ObjectIds.Int64) #NodeId, and not datatype of value. We use Int64 ID's.
        arg.ValueRank = -1
        arg.ArrayDimensions = []
        arg.Description = ua.LocalizedText(description)
        return arg
    
    # Helper method for setting up the subscription method.
    async def setup_sub_method(self):
        methods = await self.objects.add_object(self.idx, "Methods")
        print(methods)
        endp = self.method_var("Endpoint", "Address to tendpoint")
        qxvar = self.method_var("qx", "Output variable to connect to server.")
        ixvar = self.method_var("ix", "Input variable that is to be connected to.")
        ret = self.method_var("ret", "Return message for information of what happend.")
        await methods.add_method(self.idx, "subscribe", self.subscribe, [endp, qxvar, ixvar], [ret])

    # Add a local variable to the UA Server.
    async def add_variable(self, name, startvalue):
        variable = await self.varfolder.add_variable(self.idx, name, startvalue)
        print(variable)
        self.localvars[name] = [variable, startvalue]

    # Used to set a value of a variable, requires the
    # name of the variable as a string and the corresponding
    # python datatype value.
    async def write_variable(self, name, value):
        await self.localvars[name][0].write_value(value)

    # Returns the current value of the local
    # server variable.
    def get_variable_value(self, name):
        return self.localvars[name][1]

    async def update_vars(self):
        for n in self.localvars.keys():
            self.localvars[n][1] = await self.localvars[n][0].get_value()

    def add_callback(self, fnc, vars=None):
        self.callback_func = fnc
        self.callback_vars = vars

    async def go(self):
        async with self.server:
            while True:
                await asyncio.sleep(0.1)
                await self.update_vars()
                if self.callback_func is not None:
                    await self.callback_func(self.callback_vars)

if __name__ == "__main__":
    sp = ServerPI()
    asyncio.run(sp.go())
