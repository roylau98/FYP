from PyQt5 import QtCore as qtc
from datetime import datetime
from utilities.utils import process

class DataProcessor(qtc.QObject):
    result_signal = qtc.pyqtSignal(tuple)

    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue

    def process_data(self):
        while True:
            try:
                # Retrieve data from the queue (blocking call)
                data = self.data_queue.get()
                data = data.split(",")
                if data[0] == "type" and data[1] == "role" and data[2] == "mac":
                    self.result_signal.emit(("header", data))

                data[18] = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
                amp = process(data[25])

                MAC = data[2]

                if len(amp) > 0:
                    self.result_signal.emit((MAC, amp))
            except self.data_queue.Empty:
                print("Empty")