from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from opcua import Client, ua
from navigating_nodes import Navigating_nodes as navNodes

class StandardItem(Qt.QStandardItem):
    def __init__(self, txt='', font_size=10, check_box=False, set_bold=False, color=QtGui.QColor(255, 255, 255)):
        super().__init__()
        self.setEditable(False)
        self.setForeground(color)
        self.setText(txt)

        fnt = QtGui.QFont('Open Sans', font_size)
        fnt.setBold(set_bold)
        self.setFont(fnt)
        self.setCheckable(check_box)


class Client_nodes:
    def __init__(self, server, server_name):
        self.server_name = server_name
        self.Server = server
        self.client = Client("opc.tcp://" + server)

        self.ROOT_NODE = StandardItem(self.server_name, 10, True, True)
        self.MAP_VALUE_NODES = {}
        self.FOLDER_NODE = []
        self.NODE_MAP = {}
        self.NODE_ID = None
        nav_nodes = navNodes(self.client)
        try:
            self.client.connect()
            self.NODE_ID = nav_nodes.get_root_nodes()
            self.NODE_MAP.update(nav_nodes.get_name_from_nodes(nav_nodes.get_children_nodes(nav_nodes.get_root_nodes())))
        finally:
            self.client.disconnect()

        for key, values in self.NODE_MAP.items():
            for value in values:
                if key not in self.MAP_VALUE_NODES:
                    self.MAP_VALUE_NODES[key] = list()
                self.MAP_VALUE_NODES[key].append(StandardItem(value, 8, color=QtGui.QColor(180, 180, 180)))

        for key in self.MAP_VALUE_NODES:
            self.FOLDER_NODE.append(StandardItem(key, 9, color=QtGui.QColor(200, 200, 200)))
