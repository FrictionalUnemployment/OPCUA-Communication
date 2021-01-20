from tkinter import * 
from tkinter import ttk
from opcua import Client, ua

class window(Tk):
    def __init__(self):
        super(window,self).__init__()
        self.title("GUI")
        self.geometry("600x600")
        self.treetime = ttk.Treeview(self)
        self.treetime.pack()
        self.treetime.insert('', 0 , 'item1', text=ram)
        self.treetime.insert('', 0, 'item2', text=vam)   
        self.treetime.insert('', 0 , 'item3', text=par)
        self.treetime.insert('', 0 , 'item4', text=bam)

        self.treetime.move('item2', 'item1', 'end')  
        self.treetime.move('item3', 'item1', 'end')  
        self.treetime.move('item4', 'item1', 'end')  
      

if __name__ == "__main__":
    client = Client("opc.tcp://127.0.0.1:4840")
    try:
        client.connect()
        client.load_type_definitions()# load definition of server specific structures/extension objects

    
        root = client.get_root_node()
        print(root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)
        children = root.get_children()
        print(children)

        rar = client.get_node("ns=2;i=1")
        ram = rar.get_browse_name()
        print(ram)
        
        var = client.get_node("ns=2;i=2")
        vam = var.get_browse_name()
        print(vam)

        par = client.get_node("ns=2;i=3").get_browse_name()
        bam = par.__dict__['Name']

        print(bam)

        gar = client.get_node("ns=2;i=4")
        gam = gar.get_browse_name()
        print(gam)
      
    finally:
        client.disconnect()




root = window()
root.mainloop()