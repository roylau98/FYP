from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from utilities.classes import Filters, CSItype, Graphtype

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
        self.subcarrier_label = qtw.QLabel("Subcarrier: ")
        for i in range(128):
            self.subcarrier.addItem(str(i))

        self.passbandFrequency = qtw.QTextEdit()
        self.passbandFrequency.setFixedWidth(200)
        self.passbandFrequency_label = qtw.QLabel("Passband\nFrequency: ")

        self.samplingFrequency = qtw.QTextEdit()
        self.samplingFrequency.setFixedWidth(200)
        self.samplingFrequency_label = qtw.QLabel("Sampling\nFrequency (Hz): ")

        self.window_wavelet = qtw.QTextEdit()
        self.window_wavelet.setFixedWidth(200)
        self.window_wavelet_label = qtw.QLabel("Window/\nWavelet (db): ")

        self.filterButton = qtw.QPushButton("Apply filter")

        self.csi_type = qtw.QComboBox()
        self.type_label = qtw.QLabel("CSI: ")
        self.addTypes()

        self.filter_type = qtw.QComboBox()
        self.filter_label = qtw.QLabel("Filter\nType: ")
        self.addFilters()

        self.graph_type = qtw.QComboBox()
        self.graph_type_label = qtw.QLabel("Graph\nType: ")
        self.addGraphs()

        self.againstTime = qtw.QCheckBox("X-axis:\nTime")

        self.grid_layout.addWidget(self.mac_address, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.mac_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.subcarrier, 0, 3, 1, 1)
        self.grid_layout.addWidget(self.subcarrier_label, 0, 2, 1, 1)

        self.grid_layout.addWidget(self.passbandFrequency, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.passbandFrequency_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.csi_type, 1, 3, 1, 1)
        self.grid_layout.addWidget(self.type_label, 1, 2, 1, 1)

        self.grid_layout.addWidget(self.samplingFrequency_label, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.samplingFrequency, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.filter_label, 2, 2, 1, 1)
        self.grid_layout.addWidget(self.filter_type, 2, 3, 1, 1)

        self.grid_layout.addWidget(self.window_wavelet_label, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.window_wavelet, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.graph_type_label, 3, 2, 1, 1)
        self.grid_layout.addWidget(self.graph_type, 3, 3, 1, 1)
        self.grid_layout.addWidget(self.filterButton, 4, 3, 1, 1)

        self.grid_layout.addWidget(self.againstTime, 4, 0, 1, 1)

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

    def getpassbandFrequency(self):
        return float(self.passbandFrequency.toPlainText())

    def getSamplingFreq(self):
        try:
            if "Hz" in self.samplingFrequency.toPlainText():
                return int(self.samplingFrequency.toPlainText().split(" ")[0])

            return int(self.samplingFrequency.toPlainText())
        except:
            return 0

    def getAttributes(self):
        try:
            return (str(self.mac_address.currentText()), int(self.subcarrier.currentText()), self.objectName(),
                    float(self.passbandFrequency.toPlainText()), self.csi_type.currentText(), self.filter_type.currentText())
        except:
            # if cutoffFreq is not valid (empty value), dont apply butterworth filter
            return (str(self.mac_address.currentText()), int(self.subcarrier.currentText()), self.objectName(),
                    None, self.csi_type.currentText(), self.filter_type.currentText())

    def setSamplingFreq(self, samplingFreq):
        self.samplingFrequency.clear()
        self.samplingFrequency.insertPlainText(str(round(samplingFreq, 3)) + " Hz")

    def getWindowSize(self):
        return int(self.window_wavelet.toPlainText())

    def getGraphType(self):
        return self.graph_type.currentText()

    def removeFromComboBox(self):
        self.mac_address.clear()

    def addFilters(self):
        for filter in Filters:
            self.filter_type.addItem(filter.value)

    def addTypes(self):
        for type in CSItype:
            self.csi_type.addItem(type.value)

    def addGraphs(self):
        for graph in Graphtype:
            self.graph_type.addItem(graph.value)

    def againstTimeChecked(self):
        return self.againstTime.isChecked()
