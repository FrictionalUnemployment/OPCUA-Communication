#Class for navigating the nodes 

from opcua import Client, ua

#How to use the class in your own folder
#This is the import -> from ui_methods.navigating_nodes import Navigating_nodes as navNodes

#Create an instance with the client -> navigating = navNodes(client)
#Run one of the functions with your instance -> navigating.get_root_nodes()

#You could also run all of them at the same time like so:
#print(navigating.get_name_from_nodes(navigating.get_children_nodes(navigating.get_root_nodes())))
#To get the names, but best is to save every node (Cleaner code)

class Navigating_nodes:

    def __init__(self, client):
        self.client = client
        self.node_recursive_dict = list()

    def get_root_nodes(self):
        TEMP_ARRAY = []
        for i in self.client.get_objects_node().get_children()[1:]: # Skipping first element as it is unnecessary, we grab all objects in a server
            
            TEMP_ARRAY.append(i)
        
        return TEMP_ARRAY

    def get_children_nodes(self, object_array): #Gets the children nodes from the root node and adds them into a dictonary
        children_dict = {}
        temp_dict = {}
        for i in object_array:
            for j in self.client.get_node(i).get_children():
                if i not in children_dict:
                        children_dict[i] = list()
                children_dict[i].append(j)
                if len(self.client.get_node(j).get_children()) > 0:
                    if j not in temp_dict:
                        temp_dict[j] = list()
                    temp_dict[j].append(self.client.get_node(j).get_children())
                    
        if bool(temp_dict):
            self.run_recursively(temp_dict)
        return children_dict

    def run_recursively(self, map_dict):
      
        new_dict2 = {}
        for key, values in map_dict.items():
            for value in values:
                for value1 in value:
                    if len(self.client.get_node(value1).get_children()) > 0:
                        if value1 not in new_dict2:
                            new_dict2[value1] = list()
                        new_dict2[value1].append(self.client.get_node(value1).get_children())

        if bool(new_dict2):
            self.node_recursive_dict.append(map_dict)
            self.node_recursive_dict.append(new_dict2)
            self.run_recursively(new_dict2)
        
        for i in self.node_recursive_dict:
            for key, values in i.items():

                print()


    def get_rootnode_nodeid_from_name(self, root_array, children_list):
        root_childrenid_dict = {}
        for key, values in root_array.items(): #We iterate over all the root nodes and its children nodes.
            for i in children_list: # We iterate over the children string array 
                for value in values: # We check the values in the root node 
                    if key not in root_childrenid_dict:
                            root_childrenid_dict[key] = list()
                    if self.client.get_node(value).get_browse_name().__dict__['Name'] == i:
                        root_childrenid_dict[key].append(value)

    def get_name_from_nodes(self, dict_list): #Takes in a dictonary with the Objects : values that are only path values and converts to the name
        name_dict = {}
        for key, values in dict_list.items():
            for value in values:
            
                if key not in name_dict:
                    name_dict.setdefault(self.client.get_node(key).get_browse_name().__dict__['Name'], [])

                name_dict[self.client.get_node(key).get_browse_name().__dict__['Name']].append(self.client.get_node(value).get_browse_name().__dict__['Name'])
       
        return name_dict
        

#client = Client("opc.tcp://192.168.10.196:4840")
#client.connect()
#navigating = Navigating_nodes(client)
#root_nodes = navigating.get_root_nodes()
#children_nodes = navigating.get_children_nodes(root_nodes)
#print(navigating.get_name_from_nodes(navigating.get_children_nodes(navigating.get_root_nodes())))
#navigating.get_rootnode_nodeid_from_name(children_nodes, ['qxTrue', 'ixTemperature', 'ixTime'])