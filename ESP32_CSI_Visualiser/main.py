import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from userInterface.importFileWidget import importFile
from userInterface.filterWidget import filterWidget
from userInterface.logWidget import logWidget
from userInterface.mplWidget import Mpl
from utilities.utils import CSVparser, butter_lowpass_filter, hampel_filter, dwt_filter
from utilities.classes import Graphtype, CSItype, Filters, Xaxis
from sklearn.decomposition import PCA


class MainWindow(qtw.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("ESP32_CSI_Visualiser")
		self.setWindowIcon(qtg.QIcon('resources/audio-waves.png'))

		self.dataframe = None
		self.macAddresses = None
		self.CSI_DATA = {}
		self.live_data = []
		self.columns = []
		self.mplCanvas = []
		self.filterWidgets = []

		self.initUI()

	def initUI(self):
		# setups grid for the layout
		self.grid_layout = qtw.QGridLayout(self)
		self.rightgrid = qtw.QGridLayout(self)
		self.leftgrid = qtw.QGridLayout(self)
		self.buttongrid = qtw.QGridLayout(self)

		self.logWidget = logWidget()
		self.rightgrid.addWidget(self.logWidget, 0, 0)

		self.importFileWidget = importFile()
		self.importFileWidget.file.textChanged.connect(
			lambda: self.CSVparserwrapper(self.importFileWidget.getCSVFilePath()))
		self.importFileWidget.setMaximumHeight(80)
		self.rightgrid.addWidget(self.importFileWidget, 1, 0)

		self.addGraph_button = qtw.QPushButton('Add Graph', self)
		self.removeGraph_button = qtw.QPushButton('Remove Graph', self)
		self.buttongrid.addWidget(qtw.QLabel('Add/ Remove Graph:'))
		self.buttongrid.addWidget(self.addGraph_button)
		self.buttongrid.addWidget(self.removeGraph_button)
		self.addGraph_button.clicked.connect(self.addGraph)
		self.removeGraph_button.clicked.connect(self.removeGraph)

		self.rightgrid.addLayout(self.buttongrid, 2, 0)
		self.rightgrid.setColumnStretch(0, 3)

		# initialise the primary UI elements
		self.addGraph()

		self.grid_layout.addLayout(self.rightgrid, 0, 1)
		self.grid_layout.addLayout(self.leftgrid, 0, 0)

		self.setLayout(self.grid_layout)

		app.aboutToQuit.connect(self.closeEvent)

	def addGraph(self):
		if len(self.filterWidgets) < 4:
			newfilterWidget = filterWidget(len(self.filterWidgets) + 1)
			newfilterWidget.setMaximumHeight(200)

			# set the object name as the index, it will be a one to one mapping with the plot
			newfilterWidget.setObjectName(str(len(self.filterWidgets)))

			plotLambda = lambda: self.plotter(newfilterWidget)
			newfilterWidget.filterButton.clicked.connect(plotLambda)

			self.rightgrid.addWidget(newfilterWidget)
			self.filterWidgets.append(newfilterWidget)

			if len(self.filterWidgets) > 1:
				self.logWidget.insertLog(f"Added Graph {len(self.filterWidgets)}")

			newMpl_canvas = Mpl(len(self.mplCanvas) + 1)
			self.mplCanvas.append(newMpl_canvas)
			self.leftgrid.addWidget(newMpl_canvas)

			if self.macAddresses:
				print(self.macAddresses)
				newfilterWidget.addToComboBox(self.macAddresses)

	def removeGraph(self):
		# remove the last graph
		if len(self.filterWidgets) > 1:
			self.leftgrid.removeWidget(self.mplCanvas[-1])
			self.mplCanvas[-1].deleteLater()
			self.mplCanvas[-1] = None

			self.rightgrid.removeWidget(self.filterWidgets[-1])
			self.filterWidgets[-1].deleteLater()
			self.filterWidgets[-1] = None

			self.logWidget.insertLog(f"Removed Graph {len(self.filterWidgets)}")

			self.mplCanvas.pop()
			self.filterWidgets.pop()

	def CSVparserwrapper(self, CSVFile):
		self.logWidget.insertLog(f"Importing File: {CSVFile} into ESP32_CSI_Visualiser.")
		self.CSI_DATA, self.macAddresses = CSVparser(CSVFile)

		for i in self.filterWidgets:
			i.removeFromComboBox()
			i.addToComboBox(self.macAddresses)

	def plotter(self, filterWidgetObject):
		try:
			graphType = filterWidgetObject.getGraphType()
			MAC, subcarrier, index, cutoffFreq, csi_type, filter_type = filterWidgetObject.getAttributes()

			# get the amplitude or phase value
			if csi_type == CSItype.AMPLITUDE.value:
				MAC_CSI_DATA = self.CSI_DATA[MAC].getAmplitude()
			elif csi_type == CSItype.PHASE.value:
				MAC_CSI_DATA = self.CSI_DATA[MAC].getPhase()

			if graphType == Graphtype.PLOT.value or graphType == Graphtype.PCA.value:
				timeAxis = filterWidgetObject.againstTimeChecked()

				if graphType == Graphtype.PLOT.value:
					# if passband freq is none just plot normally
					self.logWidget.insertLog(f"Graph {str(int(index) + 1)}: MAC: {MAC}, subcarrier: {int(subcarrier)}, Filter: {filter_type}.")
					# MAC_CSI_DATA can be either amplitude or phase, packet x subcarrier
					Y = [x[subcarrier] for x in MAC_CSI_DATA if len(x) > subcarrier]
					Y = self.applyFilter(Y, filter_type, filterWidgetObject)
					# Y = [x[subcarrier] for x in MAC_CSI_DATA]
					if timeAxis:
						X = self.CSI_DATA[MAC].getTimeStamp()
						self.mplCanvas[int(index)].plot(X, Y, f"{csi_type} plot of subcarrier {subcarrier}", csi_type,
														subcarrier, Xaxis.TIME.value)
					else:
						X = [i + 1 for i in range(len(Y))]
						self.mplCanvas[int(index)].plot(X, Y, f"{csi_type} plot of subcarrier {subcarrier}", csi_type,
													subcarrier, Xaxis.PACKETS.value)
				else:
					self.logWidget.insertLog(f"Graph {str(int(index) + 1)}: MAC: {MAC}, Graph type: PCA, Filter: {filter_type}")
					MAC_CSI_DATA = np.array(MAC_CSI_DATA)
					pca = PCA(n_components=4)
					Y = pca.fit_transform(MAC_CSI_DATA).transpose()
					Y = self.applyFilter(Y, filter_type, filterWidgetObject)
					if timeAxis:
						X = self.CSI_DATA[MAC].getTimeStamp()
						self.mplCanvas[int(index)].PCA_plot(X, Y, csi_type, Xaxis.TIME.value)
					else:
						X = [i + 1 for i in range(len(Y))]
						self.mplCanvas[int(index)].PCA_plot(X, Y, csi_type, Xaxis.PACKETS.value)

			elif graphType == Graphtype.HEATMAP.value:
				MAC_CSI_DATA = np.array(MAC_CSI_DATA).transpose()
				self.logWidget.insertLog(f"Graph {str(int(index) + 1)}: MAC: {MAC}, Graph type: Heatmap")
				self.mplCanvas[int(index)].heatmap_plot(MAC_CSI_DATA, MAC, csi_type)
		except ValueError:
			self.logWidget.insertLog(f"Error occurred: Please import a file first or set the filters correctly.")
			return
		except Exception as e:
			msg = qtw.QErrorMessage()
			msg.showMessage(f"An error occured applying the filter due to: \n{e}.")
			msg.exec_()

	def closeEvent(self, event):
		self.logWidget.insertLog("Exiting ESP32_CSI_Visualiser")
		import sys
		sys.exit(0)

	def applyFilter(self, data, filter, filterWidgetObject):
		# dont have to apply filter
		if filter == Filters.NONE.value:
			return data

		output = []
		temp_data = np.asarray(data, dtype="float32")
		if temp_data.ndim == 1:
			data = [data]

		try:
			for Y in data:
				if filter == Filters.BUTTERWORTH.value:
					passbandFreq = filterWidgetObject.getpassbandFrequency()
					samplingFreq = filterWidgetObject.getSamplingFreq()
					Y = butter_lowpass_filter(Y, passbandFreq, samplingFreq)
				elif filter == Filters.HAMPEL.value:
					window_size = filterWidgetObject.getWindowSize()
					Y = hampel_filter(Y, window_size)
				elif "DWT" in filter:
					wavelet = filterWidgetObject.getWindowSize()
					cA, cD = dwt_filter(Y, wavelet)
					if "cA" in filter:
						Y = cA
					else:
						Y = cD
				output.append(Y)
		except:
			msg = qtw.QErrorMessage()
			msg.showMessage(f"Unable to apply {filter} filter. Please set the filters correctly.")
			msg.exec_()

		if temp_data.ndim == 1:
			return output[0]
		else:
			return output


if __name__ == '__main__':
	import sys

	app = qtw.QApplication([])
	app.setStyle('Fusion')
	qt_app = MainWindow()
	qt_app.show()
	app.exec_()
