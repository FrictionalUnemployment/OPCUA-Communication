#!/usr/bin/env python
#Credits to http://courses.compute.dtu.dk/02619/software/opcda_to_opcua.py
#Helped with the conversion of OPCDA to OPCUA

import sys, asyncio, OpenOPC, decimal, time, pywintypes
from datetime import datetime
from asyncua import ua, Server, uamethod
from zeroconf import ServiceInfo, Zeroconf
import socket

#local imports
import announce_service as sa

pywintypes.datetime = pywintypes.TimeType

UA_URI = 'https://hv.se'
OPCDA_SERVER_STRING = ""
readable_variables = {}
writeable_variables = {}
tree = {}
obj_in_node = {}


#Constants
ITEM_ACCESS_RIGHTS = 5
ACCESS_READ = 0
ACCESS_WRITE = 1
ACCESS_READ_WRITE = 2
ITEM_VALUE = 2

class SubHandler(object):
    """
    Subscription handler to receive events from the server.
    """

    def datachange_notification(self, node, val, data):
        p_a_string = node.get_path_as_string() #Get a list containing root, objects, opc da server
        da_address = '.'.join([a.split(':')[1] for a in p_a_string[3:]])
        da = OpenOPC.client()
        da.connect(OPCDA_SERVER_STRING)
        print('Datachanged ', da_address, val)
        da.write((da_address, val,))
        da.close()


def read_value(value):
	value = value[0]
	if isinstance(value,decimal.Decimal):
		value = float(value)
	elif isinstance(value,list):
		if len(value) == 0:
			value = None
	elif isinstance(value,tuple):
		if len(value) == 0:
			value = None

	return value
    
async def sort_nodes_list(list, idx, root, da):
    
    for node in list:
        parts = node.split('.') #We split it into parts to separate each "part"
        folders = parts[:-1] # The first part is the folder, typically multiple ones
        file = parts[-1]  #Then we have the file that is in the folder
        for i, folder in enumerate(folders,1):
            if i == 1:
                parent = root
                
            else:
                parent = tree[path]
            path = '.'.join(folders[0:i])
            if path not in tree.keys():
                tree[path] = await parent.add_folder(idx, folder)
        
        for id, description_of_id, value in da.properties(node):
            if id is ITEM_ACCESS_RIGHTS:
                if value == 'Read':
                    value = ACCESS_READ
                elif value == 'Write':
                    value = ACCESS_WRITE
                elif value == 'Read/Write':
                    value = ACCESS_READ_WRITE 
            obj_in_node[id] = value
        curr_value = read_value((obj_in_node[ITEM_VALUE],))
        if type(curr_value) != int:
            curr_value = 0
        
        opcua_node = await tree[path].add_variable(idx, file, ua.Variant(curr_value, ua.VariantType.UInt16))
    
        if obj_in_node[ITEM_ACCESS_RIGHTS] in [ACCESS_READ]:
            readable_variables[node] = opcua_node
            #print(opcua_node)
        if obj_in_node[ITEM_ACCESS_RIGHTS] in [ACCESS_WRITE, ACCESS_READ_WRITE]:
            await opcua_node.set_writable()        
            writeable_variables[node] = opcua_node
            #print(opcua_node)


async def main():

    #We connect to the OPC-DA server (I assume there will only be one, else this will have to be changed)
    #We can also check if there is a server and if there isn't one we'll run only an OPC UA server without conversion
    da = OpenOPC.client()
    OPCDA_SERVER_STRING = da.servers()[0]
    da.connect(OPCDA_SERVER_STRING) #Connect to the first server in the array
    print(OPCDA_SERVER_STRING)

    #Setup the server for UA
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/freeopcua/server/')
    idx = await server.register_namespace(UA_URI)
    root = await server.nodes.objects.add_object(idx,OPCDA_SERVER_STRING)
    
    #We want to find the OPC-DA server nodes in aliases
    nodes_list = da.list('*', recursive=True) #A list of dot-delimited strings
    await sort_nodes_list(nodes_list, idx, root, da)
    
    try:
        async with server: #Starting the server
            handler = SubHandler() #Subscribing to datachanges coming from the UA clients
            sub = await server.create_subscription(500, handler)
            handle = await sub.subscribe_data_change(writeable_variables.values())
            #In Robotstudio all variables are writeable, so the readable variables are empty
            #This should be changed when tried in a real environment, so temporary for now
            readable_vars = list(writeable_variables.keys()) #readable_variables
            #print(readable_vars)
        while True:
            await asyncio.sleep(1)
            for i in da.read(readable_vars):
                print(i)
                da_id = i[0]
                var_handler = writeable_variables[da_id] # Due to change
                var_handler.set_value(read_value(i[1:]))


    finally:
        await server.stop()
        da.close()

if __name__ == "__main__":
    sa.start_service_announcement()
    asyncio.run(main())