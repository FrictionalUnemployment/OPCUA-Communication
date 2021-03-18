# OPCUA-Communication
An OPC UA asynchronous application with client/server functionality for industrial systems.


#For server.py installment
You'll need Pywin32
https://github.com/mhammond/pywin32/releases
Also you need to download this .dll (Included in the wrapper folder)
When downloaded you need to open the command prompt navigate to the folder the wrapper.dll is in and run this command:
regsvr32 gbda_aut.dll

#Installing the correct libraries
Run the commands
pip3 install OpenOPC-Python3x
pip3 install asycnio
pip3 install asyncua
pip3 install PyQt5
