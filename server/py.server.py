#!/usr/bin/env python
from opcua import Server
from random import randint
import datetime
import time, sys
sys.path.insert(1, '/Users/FKV/Desktop/simpysim/OPCUA-Communication/server')
import announce_service as sa

server = Server()

url = "opc.tcp://192.168.10.196:4840"
server.set_endpoint(url)

name = "vvvvvvvvvvvvvvv"

addspace = server.register_namespace(name)

node = server.get_objects_node()
t = node.add_variable(addspace,"Lol", 0)
Params = node.add_object(addspace, "Parameters")
New_object = Params.add_object(addspace, "Ddad")
tt = New_object.add_object(addspace, "Hi")
ff = tt.add_variable(addspace, "Yoo", 0)
Params2 = node.add_object(addspace, "Params2")
Params3 = Params2.add_object(addspace, "Params5")
Params4 = Params3.add_object(addspace, "Params6")
Params5 = Params4.add_object(addspace, "Params8")
Ff = Params3.add_variable(addspace, "Hello", 0)
tt = Params4.add_variable(addspace, "ff", 0)
ttr = Params5.add_variable(addspace, "feeef", 0)
Temp = Params.add_variable(addspace, "ixTemperature",0)
Press = Params.add_variable(addspace, "ixPressure",0)
Nothing = Params.add_variable(addspace, "qxNothing",0)
Time = Params.add_variable(addspace, "ixTime",0)
Test = Params.add_variable(addspace, "ixTest",0)
Test3 = Params.add_variable(addspace, "qxTesting",0)
Test4 = Params2.add_variable(addspace, "qxTrue", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()
Test.set_writable()
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
