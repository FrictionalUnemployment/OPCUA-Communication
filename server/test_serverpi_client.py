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
        #obj = await client.nodes.root.get_child(["0:Objects", "2:Methods"])
        obj = await client.nodes.root.get_child("ns=2; i=2")
        await asyncio.sleep(0.1)

        print("Here be calling da meffod!")
        # calling a method on server

        ret = await obj.call_method("2:subscribe", "opc.tcp://0.0.0.0:4841", "ns=2;i=4", "ns=2;i=2")
        ret2 = await obj.call_method("2:subscribe", "opc.tcp://0.0.0.0:4841", "ns=2;i=5", "ns=2;i=3")

        print(ret)
        print(ret2)


if __name__ == "__main__":
    asyncio.run(main())
