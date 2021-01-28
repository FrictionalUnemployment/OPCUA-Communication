from opcua import Client, ua
from server_discovery import *



class Ui_client():
    def __init__(self, server):
        self.client = Client
        self.servers = server

    def establish_client_connection(self):

        self.client = Client("opc.tcp://" + self.servers)
        try:
            self.client.connect()
            print("client is connected: " + self.servers)

        finally:
            self.client.disconnect()



def create_connection():
    url = Server_Discovery()
    url.get_servers()
    servers = url.get_all_as_address()
    print(servers)
    established_servers = list()
    for i in servers:
        established_servers.append(Ui_client(i))
    
    established_servers[0].establish_client_connection()
    established_servers[1].establish_client_connection()
    print(established_servers[0].client.get_root_node())

        


create_connection()