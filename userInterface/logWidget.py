from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

class logWidget(qtw.QGroupBox):
    def __init__(self):
        super(logWidget, self).__init__()
        self.setTitle("Logs")
        self.initUI()

    def initUI(self):
        self.grid_layout = qtw.QGridLayout(self)

        self.logTextBox = qtw.QTextEdit()
        self.grid_layout.addWidget(self.logTextBox)

        self.setLayout(self.grid_layout)

    def insertLog(self, text):
        self.logTextBox.insertPlainText(text + "\n")

        scrollbar = self.logTextBox.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
