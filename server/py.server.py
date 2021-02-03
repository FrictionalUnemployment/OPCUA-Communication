from opcua import Server
from random import randint
import datetime
import time, sys
sys.path.insert(1, '/Users/FKV/Desktop/simpysim/OPCUA-Communication/server')
import announce_service as sa

server = Server()

url = "opc.tcp://192.168.10.196:4840"
server.set_endpoint(url)

name = "Test for GUI"

addspace = server.register_namespace(name)

node = server.get_objects_node()

Params = node.add_object(addspace, "Parameters")

Temp = Params.add_variable(addspace, "Temperature",0)
Press = Params.add_variable(addspace, "Pressure",0)
Time = Params.add_variable(addspace, "Time",0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()

#starting server
server.start()
sa.start_service_announcement(device_name="kfd347-server.",
iport=4840)

while True:
    Temperature = randint(0,35)
    Pressure = randint(100,250)
    TIME = datetime.datetime.now()

    print(Temperature,Pressure,TIME)

    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(TIME)

    time.sleep(5)
