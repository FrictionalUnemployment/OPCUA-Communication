from opcua import Client, ua
from ui_methods.server_discovery import *
import time



class Ui_client():
    def __init__(self):
        self.client = Client

    
    def discover_servers(self):
        url = Server_Discovery()
        servers = url.get_servers()
        print(servers)


    def pick_server(self):
        
        sd = Server_Discovery()
        sd.get_servers()
        print("Enter the Ip:Port to the server you wanna connect to")
        server_url = input() #ip and port
        if server_url in sd.get_all_as_address():
            client = Client("opc.tcp://" + server_url)
            client.connect()
            print("client is connected")
        else:
             print("ip doesnt exist")


        



    
    



  #  def client_connection(self, url):
    
        
        #url_a = url.get_all(1) + url.get_all(2)
        #url = ':'.join(map(str, url_a))
      #  print(url)
        

       #client = Client("opc.tcp://" + url)

        #try:
           # client.connect()
          #  if True:
           #    print("Client is now connected to the server")
                
           # else:
            #   print("The client cannot connect to the server")

      #  finally:
          #  client.disconnect()
    

    
        
        
        
if __name__ =="__main__":
    Ui_client().discover_servers()
    Ui_client().pick_server()
    
    

    