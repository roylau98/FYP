from PyQt5 import QtWidgets as qtw

from pathlib import Path
import os

class importFile(qtw.QGroupBox):
    def __init__(self):
        super(importFile, self).__init__()
        self.setTitle(f"Import File")
        self.initUI()

    def initUI(self):
        self.grid_layout = qtw.QGridLayout(self)

        self.file_browser_btn = qtw.QPushButton('Browse')
        self.file_browser_btn.clicked.connect(self.openFileDialog)
        self.grid_layout.addWidget(self.file_browser_btn)

        self.file = qtw.QTextEdit(self)
        self.file.setReadOnly(True)
        self.file.setFixedHeight(25)

        self.grid_layout.addWidget(qtw.QLabel('File:'), 0, 0)
        self.grid_layout.addWidget(self.file, 0, 1)
        self.grid_layout.addWidget(self.file_browser_btn, 0, 2)

        self.setLayout(self.grid_layout)

    def openFileDialog(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self,
            "Select a File",
            os.getcwd(),
            "CSV File (*.csv)"
        )

        if filename:
            path = Path(filename)
            self.file.setText(str(path))

    def getCSVFileName(self):
        return self.file.toPlainText()
