#/usr/bin/env python3

# This file contains a set of classes and methods to handle
# running a OPC UA server on a raspberry pi.


import asyncio
import random
from asyncua import ua, uamethod, Server
import announce_service as sa

SERVER_NAME = "RaspPI OPC UA Server"
FLAT_NAME = SERVER_NAME.replace(" ", "")
SERVER_ENDPOINT = "opc.tcp://0.0.0.0:4840/raspua/server"
UA_NAMESPACE = "hvproj:ua:"+FLAT_NAME
TEMP = 19

class ServerPI:

    def __init__(self):
        self.temp = TEMP

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
        zvar = await zobj.add_variable(idx, "Temperature", self.temp)

        async with server:
            while True:
                await asyncio.sleep(0.1)
                await zvar.write_value(self.temp)
                self.temp = 19 + random.random()


if __name__ == "__main__":
    sa.start_service_announcement()
    sp = ServerPI()
    asyncio.run(sp.go())
