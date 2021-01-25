from opcua import Client
from discovery import Discovery
import time

url = "opc.tcp://127.0.0.1:4840"

client = Client(url)

#connecting client to server
client.connect()


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("GUI for client")
        self.minsize(400,200)

        self.button = ttk.Button(self, text="Press4Temperature",command = self.clickbutton)
        self.button.grid(column=0, row=0)

        self.pressurebutton = ttk.Button(self,text="Press4Pressure", command = self.clickbutton2)
        self.pressurebutton.grid(column=0, row = 1)

        self.datetimebutton = ttk.Button(self,text="Press4Datetime", command = self.clickbutton3)
        self.datetimebutton.grid(column=0, row = 2)

          


        self.label = ttk.Label(self, text="The temperature is:")
        self.label.grid(column=1, row=0)

        self.label = ttk.Label(self, text="The Pressure is:")
        self.label.grid(column=1, row=1)

        self.label = ttk.Label(self, text="The Datetime is:")
        self.label.grid(column=1, row=2)



    def clickbutton(self):
        self.Temp = client.get_node("ns=2;i=2")
        Temperature = self.Temp.get_value()
        self.label = ttk.Label(self, text=Temperature)
        self.label.grid(column=3, row=0)
    
       

    def clickbutton2(self):
        self.Press = client.get_node("ns=2;i=3")
        Pressure = self.Press.get_value()
        self.label = ttk.Label(self, text=Pressure)
        self.label.grid(column=3, row=1)

       

    def clickbutton3(self):
        self.Time = client.get_node("ns=2;i=4")
        TIME = self.Time.get_value()
        self.label = ttk.Label(self, text=TIME)
        self.label.grid(column=3, row=2)
   
        
    


root = Root()
root.mainloop()
