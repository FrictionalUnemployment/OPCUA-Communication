# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zuo.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from zeroconf import ServiceBrowser, Zeroconf
import server_discovery as dsc
import Ui_client as ui_c
import client_nodes as cl_node
from client_nodes import StandardItem as StItem
import navigating_nodes as nav
import sys

class Node_storage:
    def __init__(self, node_name, node_id, standarditem):
        self.node_name = node_name
        self.node_id = node_id
        self.standarditem = standarditem

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.clients = list()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1014, 513)
        MainWindow.setStyleSheet("background-color: rgb(200, 200, 200;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Connect = QtWidgets.QPushButton(self.centralwidget)
        self.Connect.setGeometry(QtCore.QRect(780, 0, 81, 21))
        self.Connect.setStyleSheet("color: rgb(0, 0, 0);")
        self.Connect.clicked.connect(self.manual_connection)
        self.Connect.setObjectName("Connect")
       
        self.Discover = QtWidgets.QPushButton(self.centralwidget)
        self.Discover.setGeometry(QtCore.QRect(690, 0, 81, 21))
        self.Discover.setStyleSheet("color: rgb(0, 0, 0);")
        self.Discover.clicked.connect(self.discover_servers)
        self.Discover.setObjectName("Discover")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 0, 681, 21))
        self.lineEdit.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit.setObjectName("lineEdit")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(340, 20, 611, 331))
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("color: rgb(0,0,0);")

      

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 360, 942, 111))
        self.textBrowser.setObjectName("textBrowser")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(870, 0, 81, 21))
        self.pushButton.setStyleSheet("color: rgb(0, 0, 0);")
        self.pushButton.setObjectName("pushButton")

        self.pairingbutton = QtWidgets.QPushButton(self.centralwidget)
        self.pairingbutton.setGeometry(QtCore.QRect(960, 0, 81, 21))
        self.pairingbutton.setStyleSheet("color: rgb(0, 0, 0);")
        self.pairingbutton.setObjectName("pairButton")
        self.pairingbutton.hide()

        
        
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(10, 26, 331, 325))
        self.treeView.setObjectName("treeView")

        self.right_treeView = QtWidgets.QTreeView(self.centralwidget)
        self.right_treeView.setGeometry(QtCore.QRect(951, 26, 331, 325))
        self.right_treeView.setObjectName("Right_treeview")
        self.right_treeView.hide()

        self.Connect.raise_()
        self.Discover.raise_()
        self.lineEdit.raise_()
        self.textBrowser.raise_()
        self.pushButton.raise_()
        self.treeView.raise_()
        self.groupBox.raise_()  
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.closing_app = QtWidgets.QAction(MainWindow)
        self.closing_app.setObjectName("Closing Application")
        self.closing_app.setShortcut("CTRL+Q")
        self.closing_app.triggered.connect(self.closing_application)
        self.actionRight_Hand_tree = QtWidgets.QAction(MainWindow)
        self.actionRight_Hand_tree.setObjectName("actionRight_Hand_tree")
        self.actionRight_Hand_tree.setShortcut("CTRL+N")
        self.actionRight_Hand_tree.triggered.connect(self.creating_right_window)
        self.hide_Right_Hand_tree = QtWidgets.QAction(MainWindow)
        self.hide_Right_Hand_tree.setObjectName("Hiding tree")
        self.hide_Right_Hand_tree.setShortcut("CTRL+M")
        self.hide_Right_Hand_tree.triggered.connect(self.closing_right_window)
 
        self.menuFile.addAction(self.closing_app)
        self.menuView.addAction(self.actionRight_Hand_tree)
        self.menuView.addAction(self.hide_Right_Hand_tree)
      
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
       
        ############################### Discovery ################################

        self.treeModel = Qt.QStandardItemModel()
        self.treeView.setHeaderHidden(True)
        self.rootNode = self.treeModel.invisibleRootItem()
        self.treeView.setModel(self.treeModel)
        self.treeView.doubleClicked.connect(self.getValueLeft)

        ###### Right hand tree #######
        self.right_treeView.setModel(self.treeModel)
        self.right_treeView.doubleClicked.connect(self.getValueRight)


        ## LINKING ##
        self.left_server = None
        self.right_server = None

        ## VARIABLES #####
        self.ROOT_CHILDREN_NODES = []

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CustomOPC"))
        self.Connect.setText(_translate("MainWindow", "Connect"))
        self.Discover.setText(_translate("MainWindow", "Discover"))
        self.groupBox.setTitle(_translate("MainWindow", "Attribute Panel"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Disconnect"))
        self.pairingbutton.setText(_translate("MainWindow", "Pair"))
      
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionRight_Hand_tree.setText(_translate("MainWindow", "Expand a right hand tree"))
        self.hide_Right_Hand_tree.setText(_translate("MainWindow", "Hide the right hand tree"))
        self.closing_app.setText(_translate("MainWindow", "Quit"))


    def closing_application(self):
        QtWidgets.qApp.quit()

    
    def getValueLeft(self, val):
        node_name = val.data()
        bool_continue = True
        for i in self.clients:
            if(i.server_name == node_name):
                for k in i.NODE_ID:
                    for j in self.ROOT_CHILDREN_NODES:
                        i.client.connect()
                        children_name = i.client.get_node(k).get_browse_name().__dict__['Name']
                        if(children_name == j.node_name):
                            bool_continue = False
                            break
        
        for i in self.clients:
            for j in self.ROOT_CHILDREN_NODES:
                if(node_name == j.node_name):
                    i.client.connect()
                    for d in i.client.get_node(j.node_id).get_children():
                        children_name = i.client.get_node(d).get_browse_name().__dict__['Name']
                        print(children_name)
                        for k in self.ROOT_CHILDREN_NODES:
                            if(children_name == k.node_name):
                                bool_continue = False
                                break 

        for i in self.clients:
            if(i.server_name == node_name and bool_continue == True):
                
                for j in i.NODE_ID:
                    i.client.connect()
                    children_name = i.client.get_node(j).get_browse_name().__dict__['Name']
                    qtitem = StItem(children_name, 8, color=QtGui.QColor(180, 180, 180))
                    i.ROOT_NODE.appendRow(qtitem)
                    self.ROOT_CHILDREN_NODES.append(Node_storage(children_name, j, qtitem))

    
        for i in self.clients:
            for j in self.ROOT_CHILDREN_NODES:
                
                if(node_name == j.node_name and bool_continue == True):
                    
                    i.client.connect()
                    for d in i.client.get_node(j.node_id).get_children():
                        #    printif(i.client.get_node(d).get_children() == 0):
                        
                        children_name = i.client.get_node(d).get_browse_name().__dict__['Name']
                        
                        qtitem = StItem(children_name, 8, color=QtGui.QColor(180, 180, 180))
                        j.standarditem.appendRow(qtitem)
                        self.ROOT_CHILDREN_NODES.append(Node_storage(children_name, d, qtitem))
                            #self.treeView.selectedIndexes()[0].model().itemFromIndex(val).appendRow(StItem(children_name, 8, color=QtGui.QColor(180, 180, 180)))
  

    def LinkValueLeft(self, val):
        if(val.parent()):
            SERVER_NAME = val.data()

        print(SERVER_NAME)
        if(self.left_server == None and val.parent()):
            for i in self.clients:
                if(i.server_name == SERVER_NAME):
                    self.left_server = i
                    self.textBrowser.append("Linked server to the left to: " + SERVER_NAME)
        else:
            self.textBrowser.append("Unlinked server to the left for: " + SERVER_NAME)
            self.left_server = None

    def getValueRight(self, val):
        if(val.parent()):
            SERVER_NAME = val.data()

        if(self.right_server == None and val.parent()):
            for i in self.clients:
                if(i.server_name == SERVER_NAME):
                    self.right_server = i
                    self.textBrowser.append("Linked server to the right to: " + SERVER_NAME)
        else:
            self.textBrowser.append("Unlinked server to the right for: " + SERVER_NAME)
            self.right_server = None
        #Left ix Pressure -> qx Pressure Right
        #Left qx Temperature <- ix Temperature Right
        if(self.right_server != None and self.left_server != None):
            server1_lst = list([j for i in self.left_server.NODE_MAP.values() for j in i])
            server2_lst = list([j for i in self.right_server.NODE_MAP.values() for j in i])
            result1 = filter(lambda x: 'ix' in x, server1_lst)
            result2 = filter(lambda x: 'qx' in x, server2_lst)  
            print(list(result1))
            print(list(result2))
            
           # for i,j in itertools.zip_longest(list([j for i in self.right_server.NODE_MAP.values() for j in i]), 
            #        list([j for i in self.left_server.NODE_MAP.values() for j in i])):
            #    print(i,j )
            

    def creating_right_window(self):
        MainWindow.resize(1300, 513) # resizing the window to be able to fit the new treeview
        self.textBrowser.resize(1272, 111) # making the textbox bigger to be able to display more information
        self.right_treeView.show()
        self.pairingbutton.show()    
    

    def closing_right_window(self):
        self.right_treeView.hide()
        self.textBrowser.resize(942, 111)
        self.pairingbutton.hide()


    def manual_connection(self):
        manually_entered_server = self.lineEdit.text()
        url = dsc.Server_Discovery()
        url.get_servers()
        servers = url.get_all_as_address()
    
        if manually_entered_server in servers:
            self.textBrowser.append("Server:" + manually_entered_server + " found and connected.")
        

        else:
            self.textBrowser.append("no server found")
      
        
        
      


    def discover_servers(self):
        if len(self.clients) > 0:
            self.clients.clear()
            self.treeModel.removeRows(0, self.treeModel.rowCount())

        url = dsc.Server_Discovery()
        url.get_servers()
        self.SERVER_ARR = url.get_all(0)
        servers = url.get_all_as_address()
        

        j = 0
        for i in servers:
            self.clients.append(cl_node.Client_nodes(i, self.SERVER_ARR[j]))
            self.textBrowser.append("Service added: " + self.SERVER_ARR[j] + "- At address: " + i)

            j += 1

        for i in self.clients:
            self.rootNode.appendRow(i.ROOT_NODE)


        

    

            
        
        

if __name__ == "__main__":
   
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())
