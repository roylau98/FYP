import sys
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from queue import Queue

class DataProcessor(QObject):
    result_signal = pyqtSignal(str)

    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue

    def process_data(self):
        while True:
            try:
                # Retrieve data from the queue (blocking call)
                data = self.data_queue.get()
                result = f"Processed data: {data.upper()}"
                self.result_signal.emit(result)
            except self.data_queue.Empty:
                print("Empty")

class WorkerThread(QThread):
    data_signal = pyqtSignal(str)
    stop_signal = pyqtSignal()

    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue

    def run(self):
        while True:
            try:
                sys.stdin.buffer.flush()
                output = sys.stdin.buffer.readline().decode('utf-8').replace("\n", "").replace("\r", "")
                if "CSI_DATA" in output:
                    self.data_signal.emit(output)
            except:
                pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data_queue = Queue()  # Thread-safe queue for streaming data
        self.worker_thread = WorkerThread(self.data_queue)
        self.data_processor = DataProcessor(self.data_queue)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Data will be displayed here", self)
        layout.addWidget(self.label)

        start_button = QPushButton("Start Thread", self)
        start_button.clicked.connect(self.start_threads)
        layout.addWidget(start_button)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("Thread Communication Example")
        self.show()

    def start_threads(self):
        # Connect the signals and start the threads
        self.worker_thread.data_signal.connect(self.update_label)
        self.worker_thread.stop_signal.connect(self.stop_data_processor)
        self.worker_thread.start()

        # Start the data processor
        self.data_processor.result_signal.connect(self.update_label)
        self.data_processor_thread = QThread()
        self.data_processor.moveToThread(self.data_processor_thread)
        self.data_processor_thread.started.connect(self.data_processor.process_data)
        self.data_processor_thread.start()

    def stop_data_processor(self):
        # Stop the data processor when the worker thread has finished producing data
        self.data_processor_thread.quit()
        self.data_processor_thread.wait()

    def update_label(self, data):
        # Slot to update the label with data received from the worker thread or DataProcessor
        self.label.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())