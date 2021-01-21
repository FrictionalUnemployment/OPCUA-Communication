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


    def get_root_nodes(self):
        TEMP_ARRAY = []
  
        for i in self.client.get_objects_node().get_children()[1:]: # Skipping first element as it is unnecessary, we grab all objects in a server

            TEMP_ARRAY.append(i)
    
        return TEMP_ARRAY

    def get_children_nodes(self, object_array): #Gets the children nodes from the root node and adds them into a dictonary
        CHILDREN_NODE_DICT = {}

        for i in object_array:
            for j in self.client.get_node(i).get_children():
                if i not in CHILDREN_NODE_DICT:
                    CHILDREN_NODE_DICT[i] = list()
                CHILDREN_NODE_DICT[i].append(j)
            
        return CHILDREN_NODE_DICT

    def get_name_from_nodes(self, dict_list): #Takes in a dictonary with the Objects : values that are only path values and converts to the name
        name_dict = {}
        for key, values in dict_list.items():
            for value in values:
            
                if key not in name_dict:
                    name_dict.setdefault(self.client.get_node(key).get_browse_name().__dict__['Name'], [])

                name_dict[self.client.get_node(key).get_browse_name().__dict__['Name']].append(self.client.get_node(value).get_browse_name().__dict__['Name'])
       
        return name_dict
