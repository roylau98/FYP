import seaborn as sns
from PyQt5 import QtWidgets as qtw

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from utilities.classes import Xaxis

class Mpl(qtw.QGroupBox):
    def __init__(self, id):
        super(Mpl, self).__init__()
        self.setTitle(f"Graph {id}")
        self.setFixedWidth(1000)
        self.initUI()

    def initUI(self):
        self.fig = Figure(figsize=(10, 6), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout = qtw.QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

    def plot(self, X, Y, label, csi_type, subcarrier, x_axis):
        # remove the entire plot
        # self.ax.remove()
        self.fig.clear()

        self.ax = self.canvas.figure.add_subplot(111)
        self.canvas.draw()
        if x_axis == Xaxis.PACKETS.value:
            self.ax.plot(tuple(X), tuple(Y), label=label)
        else:
            self.ax.scatter(X, Y, s=3)

        self.ax.set_title(f"CSI {csi_type} of subcarrier {subcarrier}")
        self.ax.set_xlabel(f"{x_axis}")

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

    def PCA_plot(self, X, Y, csi_type, x_axis):
        """
        Plots the top k=4 principal components of the CSI data
        :param X:
        :param Y:
        :param csi_type:
        :param x_axis:
        :return:
        """
        self.fig.clear()

        self.canvas.draw()
        self.fig.suptitle(f"PCA of CSI {csi_type}")
        for i in range(4):
            self.ax = self.canvas.figure.add_subplot(2, 2, i+1)
            if x_axis == Xaxis.PACKETS.value:
                self.ax.plot(Y[i], label=f"PCA {i}")
            else:
                self.ax.scatter(X, Y[i], s=3)
            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(f"PCA {i+1}")
            self.ax.set_title(f"({chr(97 + i)})")

        self.canvas.draw()
