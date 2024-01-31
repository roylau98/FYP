from PyQt5 import QtWidgets as qtw

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class Mpl(qtw.QGroupBox):
    def __init__(self, id):
        super(Mpl, self).__init__()
        self.setTitle(f"Graph {id}")
        self.initUI()

    def initUI(self):
        fig = Figure(figsize=(5, 5))
        self.canvas = FigureCanvasQTAgg(fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout = qtw.QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

    def plot(self, X, Y, label):
        self.ax.cla()
        self.ax.plot(tuple(X), tuple(Y), label=label)
        self.ax.set_xlabel("Number of packets")
        self.ax.set_ylabel("CSI Amplitude")
        self.canvas.draw()