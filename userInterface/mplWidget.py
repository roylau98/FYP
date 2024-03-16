import seaborn as sns
from PyQt5 import QtWidgets as qtw

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class Mpl(qtw.QGroupBox):
    def __init__(self, id):
        super(Mpl, self).__init__()
        self.setTitle(f"Graph {id}")
        self.initUI()

    def initUI(self):
        self.fig = Figure(figsize=(10, 6), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout = qtw.QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

    def plot(self, X, Y, label, csi_type, subcarrier):
        # remove the entire plot
        # self.ax.remove()
        self.fig.clear()

        self.ax = self.canvas.figure.add_subplot(111)
        self.canvas.draw()
        self.ax.plot(tuple(X), tuple(Y), label=label)
        self.ax.set_title(f"CSI {csi_type} of subcarrier {subcarrier}")
        self.ax.set_xlabel("Number of packets")

        self.ax.set_ylabel(f"CSI {csi_type}")
        self.canvas.draw()

    def heatmap_plot(self, CSI_DATA, MAC, csi_type):
        # self.ax.remove()
        self.fig.clear()
        self.ax = self.canvas.figure.add_subplot(111)
        self.canvas.draw()
        sns.heatmap(ax=self.ax, data=CSI_DATA)
        self.ax.set_title(f"Heatmap of CSI {csi_type}")
        self.ax.set_ylabel("Subcarriers")
        self.ax.set_xlabel(f"Packet index")
        self.canvas.draw()

    def PCA_plot(self, pca_data, csi_type):
        self.fig.clear()

        self.canvas.draw()
        self.ax.set_title(f"PCA of CSI {csi_type}")
        for i in range(4):
            self.ax = self.canvas.figure.add_subplot(2, 2, i+1)
            self.ax.plot(pca_data[i], label=f"PCA {i}")
            self.ax.set_xlabel("Packets")
            self.ax.set_ylabel("CSI Amplitude")
            self.ax.set_title(f"({chr(97 + i)})")

        self.canvas.draw()
