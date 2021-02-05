#DISCOVER ALL SERVERS WITH THIS METHOD.
import discovery as disc
import time
# For testing:
#d = Server_Discovery() # Create an instance

#print(d.get_servers()) #Get all servers available in a tuple

#print(d.get_all(1)) # Get all ip addresses from all servers

class Server_Discovery():
    def __init__(self):
        self.DISCOVERY_OUTPUT = []

    def get_servers(self): # To find the servers available

        Test_types = ["_opcua-tcp._tcp.local.",
                    "_opcua-https._tcp.local.",
                    "_opcua-wss._tcp.local."]

        d = disc.Discovery(Test_types)
        time_to_end = time.time() + 5
        while(time.time() < time_to_end):
            if(len(d.get_services()) > 0):
                self.DISCOVERY_OUTPUT = d.get_services()

        return self.DISCOVERY_OUTPUT

    def get_all(self, type): #0 for server name, 1 for ip address, 2 for port number
        temp_array = []
        for i in self.DISCOVERY_OUTPUT:
            temp_array.append(i[type])

        return temp_array

    def combine(self, server):
        return server[1] + ":" + server[2]

    def get_all_as_address(self):
        arr = []
        for s in self.DISCOVERY_OUTPUT:
            arr.append(self.combine(s))

        return arr