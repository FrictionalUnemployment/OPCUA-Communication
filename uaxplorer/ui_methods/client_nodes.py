from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from opcua import Client, ua
from navigating_nodes import Navigating_nodes as navNodes

class StandardItem(Qt.QStandardItem):
    def __init__(self, txt='', font_size=10, set_bold=False, color=QtGui.QColor(255, 255, 255)):
        super().__init__()
        self.setEditable(False)
        self.setForeground(color)
        self.setText(txt)

        fnt = QtGui.QFont('Open Sans', font_size)
        fnt.setBold(set_bold)
        self.setFont(fnt)


class Client_nodes:
    def __init__(self, server, server_name):
        self.server_name = server_name
        self.Server = server
        self.client = Client("opc.tcp://" + server)

        self.ROOT_NODE = StandardItem(self.server_name, 12, True, color=QtGui.QColor(128, 128, 128))
        self.MAP_VALUE_NODES = {}
        self.FOLDER_NODE = []

        NODE_MAP = {}
        nav_nodes = navNodes(self.client)
        try:
            self.client.connect()
            NODE_MAP.update(nav_nodes.get_name_from_nodes(nav_nodes.get_children_nodes(nav_nodes.get_root_nodes())))

        finally:
            self.client.disconnect()

        for key, values in NODE_MAP.items():
            for value in values:
                if key not in self.MAP_VALUE_NODES:
                    self.MAP_VALUE_NODES[key] = list()
                self.MAP_VALUE_NODES[key].append(StandardItem(value, 10))

        for key in self.MAP_VALUE_NODES:
                self.FOLDER_NODE.append(StandardItem(key))