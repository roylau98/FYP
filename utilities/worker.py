from PyQt5 import QtCore as qtc

import sys

class Worker(qtc.QObject):
    finished = qtc.pyqtSignal()
    progress = qtc.pyqtSignal(str)

    def run(self):
        while True:
            try:
                sys.stdin.buffer.flush()
                output = sys.stdin.buffer.readline().decode('utf-8').replace("\n", "").replace("\r", "")
                if "CSI_DATA" in output:
                    self.progress.emit(output)
            except:
                pass
                
    def stop(self):
        self.threadactive = False
        self.wait()
