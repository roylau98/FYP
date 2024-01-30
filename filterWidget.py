from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class filterWidget(qtw.QGroupBox):
    def __init__(self, id):
        super(filterWidget, self).__init__()
        self.setTitle(f"Graph {id}")
        self.initUI()
        self.index = 1

    def initUI(self):
        self.grid_layout = qtw.QGridLayout(self)

        self.mac_address = qtw.QComboBox()
        self.mac_label = qtw.QLabel("MAC: ")
        self.mac_address.setFixedWidth(200)

        self.subcarrier = qtw.QComboBox()

        for i in range(256):
            self.subcarrier.addItem(str(i+1))

        self.subcarrier_label = qtw.QLabel("Subcarrier: ")

        self.grid_layout.addWidget(self.mac_address, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.mac_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.subcarrier, 0, 3, 1, 1)
        self.grid_layout.addWidget(self.subcarrier_label, 0, 2, 1, 1)
        self.setLayout(self.grid_layout)

    def addToComboBox(self, listOfMAC):
        for i in listOfMAC:
            self.mac_address.addItem(i)

    def getMac(self):
        return str(self.mac_address.currentText())

    def getSubcarrier(self):
        return int(self.subcarrier.currentText())

    def getindex(self):
        return self.objectName()

    def getAttributes(self):
        return str(self.mac_address.currentText()), int(self.subcarrier.currentText()), self.objectName()