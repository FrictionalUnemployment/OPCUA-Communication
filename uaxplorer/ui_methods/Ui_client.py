from opcua import Client, ua
import server_discovery as disc



class Ui_client():
    def __init__(self, server):
        self.client = Client("opc.tcp://" + server)
        self.servers = server

def create_connection():
    url = disc.Server_Discovery()
    url.get_servers()
    servers = url.get_all_as_address()
    print(servers)
    established_servers = list()
    for i in servers:
        established_servers.append(Ui_client(i))
    
    return established_servers

