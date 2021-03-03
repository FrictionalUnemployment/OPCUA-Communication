import asyncio

from asyncua import Client

SERVER_NAME = "RaspPI OPC UA Server"
FLAT_NAME = SERVER_NAME.replace(" ", "")
SERVER_ENDPOINT = "opc.tcp://0.0.0.0:4840"
UA_NAMESPACE = "hvproj:ua:"+FLAT_NAME
TEMP = 19

class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)


async def main():
    url = "opc.tcp://0.0.0.0:4840"
    async with Client(url=url) as client:
        #uri = "UA_NAMESPACE"
        #idx = await client.get_namespace_index(uri)
        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #await var.read_data_value() # get value of node as a DataValue object
        #await var.read_value() # get value of node as a python builtin
        #await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #await var.write_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        myvar = await client.nodes.root.get_child(["0:Objects", "2:Sensors", "2:ixTemperature"])
        obj = await client.nodes.root.get_child(["0:Objects", "2:Methods"])
        # subscribing to a variable node
        handler = SubHandler()
        sub = await client.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(myvar)
        await asyncio.sleep(0.1)

        # we can also subscribe to events from server
        await sub.subscribe_events()
        # await sub.unsubscribe(handle)
        # await sub.delete()
        print("Here be calling da meffod!")
        # calling a method on server
        ret = await obj.call_method("2:subscribe", "opc.tcp://0.0.0.0:4841", "ns=2;i=3", "ixtemp")
        print(ret)


if __name__ == "__main__":
    asyncio.run(main())
