from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from userInterface.importFileWidget import importFile
from userInterface.filterWidget import filterWidget
from userInterface.logWidget import logWidget
from userInterface.mplWidget import Mpl
from utilities.worker import Worker
from utilities.utils import process, CSVparser, butter_lowpass_filter

import pandas as pd
from datetime import datetime

live = False
startTime = None

class MainWindow(qtw.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("ESP32 CSI Visualiser")
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

		self.logWidget = logWidget()
		self.rightgrid.addWidget(self.logWidget)

		self.importFileWidget = importFile()
		self.importFileWidget.file.textChanged.connect(
			lambda: self.CSVparserwrapper(self.importFileWidget.getCSVFileName()))
		self.importFileWidget.setMaximumHeight(80)
		self.rightgrid.addWidget(self.importFileWidget)

		self.addGraph_button = qtw.QPushButton('Add Graph', self)
		self.removeGraph_button = qtw.QPushButton('Remove Graph', self)

		self.rightgrid.addWidget(self.addGraph_button)
		self.addGraph_button.clicked.connect(self.addGraph)
		self.rightgrid.addWidget(self.removeGraph_button)
		self.removeGraph_button.clicked.connect(self.removeGraph)

		# initialise the primary UI elements
		self.addGraph()

		self.grid_layout.addLayout(self.rightgrid, 0, 1)
		self.grid_layout.addLayout(self.leftgrid, 0, 0)
		self.setLayout(self.grid_layout)

		app.aboutToQuit.connect(self.closeEvent)

		if live:
			self.logWidget.insertLog("Starting ESP32 CSI Visualiser in live plotting mode")
			global startTime
			startTime = datetime.now()

			self.read_thread = qtc.QThread()
			self.worker = Worker()
			self.worker.moveToThread(self.read_thread)
			self.read_thread.started.connect(self.worker.run)
			self.worker.finished.connect(self.read_thread.quit)
			self.worker.finished.connect(self.worker.deleteLater)
			self.worker.progress.connect(self.reportProgress)
			# Step 6: Start the thread
			self.read_thread.start()
			
			self.live_plottingtimer = qtc.QTimer()
			self.live_plottingtimer.timeout.connect(self.live_plotting)
			self.live_plottingtimer.setInterval(1000)
			self.live_plottingtimer.start()

	def addGraph(self):
		if len(self.filterWidgets) < 4:
			print("Added graph")
			newfilterWidget = filterWidget(len(self.filterWidgets) + 1)
			newfilterWidget.setMaximumHeight(140)

			# set the object name as the index, it will be a one to one mapping with the plot
			newfilterWidget.setObjectName(str(len(self.filterWidgets)))

			if not live:
				# need to use lambdas to send arguments
				plotLambda = lambda: self.plotter(newfilterWidget)
				#newfilterWidget.mac_address.currentTextChanged.connect(plotLambda)
				#newfilterWidget.subcarrier.currentTextChanged.connect(plotLambda)

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


	def live_plotting(self):
		for idx in range(len(self.filterWidgets)):
			filterWidgetObject = self.filterWidgets[idx]
			MAC, subcarrier, index, cutoffFreq = filterWidgetObject.getAttributes()
			if MAC == "":
				return
			diff = (datetime.now() - startTime).total_seconds()

			self.CSI_DATA[MAC]["frequency"] = len(self.CSI_DATA[MAC]["amplitudes"]) / diff
			self.filterWidgets[idx].setSamplingFreq(self.CSI_DATA[MAC]["frequency"])
			samplingFreq = self.CSI_DATA[MAC]["frequency"]
			# list of list of CSI data
			csi = self.CSI_DATA[MAC]["amplitudes"]
			# get the last 200 lists to plot
			csi = csi[-200:]

			Y = [x[subcarrier] for x in csi if len(x) > subcarrier]

			try:
				if cutoffFreq:
					Y = butter_lowpass_filter(Y, cutoffFreq, samplingFreq)
			except:
				pass
			X = [i + 1 for i in range(len(Y))]

			self.mplCanvas[idx].plot(X, Y, f"Amplitude plot of subcarrier {subcarrier}")
		

	def reportProgress(self, result):
		result = result.split(",")
		
		if len(self.columns) == 0:
			self.columns = result
			return
		
		try:
			result[18] = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
			self.live_data.append(result)
			amp = process(result[25])
			
			MAC = result[2]
				
			if len(amp) > 0:
				if MAC in self.CSI_DATA:
					self.CSI_DATA[MAC]["amplitudes"].append(amp)
					# self.CSI_DATA[MAC]["frequency"] = len(self.CSI_DATA[MAC]["amplitudes"]) / diff
				else:
					self.CSI_DATA[MAC] = {"amplitudes": [amp], "frequency": 0}
					
					for filterWidget in self.filterWidgets:
						filterWidget.addToComboBox([MAC])
						
					if self.macAddresses == None:
						self.macAddresses = [MAC]
					
					if self.macAddresses and MAC not in self.macAddresses:
						self.macAddresses.append(MAC)
						
		except:
			return
				

	def CSVparserwrapper(self, CSVFile):
		self.logWidget.insertLog(f"Importing File: {CSVFile} into ESP32 CSI Visualiser.")
		self.CSI_DATA, self.macAddresses = CSVparser(CSVFile)

		for i in self.filterWidgets:
			i.addToComboBox(self.macAddresses)

	def plotter(self, filterWidgetObject):
		if live == False:
			try:
				# if cutoff freq is none just plot normally
				MAC, subcarrier, index, cutoffFreq = filterWidgetObject.getAttributes()
				samplingFreq = self.CSI_DATA[MAC]["frequency"]
				self.filterWidgets[int(index)].setSamplingFreq(samplingFreq)
				self.logWidget.insertLog(f"Graph {str(int(index) + 1)}: MAC - {MAC}, subcarrier - {int(subcarrier)},"
										 f"sampling frequency - {str(round(samplingFreq, 2))} (Hz), "
										 f"cutoff frequency {str(cutoffFreq)}.")

				amplitudes = self.CSI_DATA[MAC]["amplitudes"]
				Y = [x[subcarrier] for x in amplitudes if len(x) > subcarrier]

				if cutoffFreq:
					Y = butter_lowpass_filter(Y, cutoffFreq, samplingFreq)

				X = [i + 1 for i in range(len(Y))]
				self.mplCanvas[int(index)].plot(X, Y, f"Amplitude plot of subcarrier {subcarrier}")
			except ValueError:
				self.logWidget.insertLog(f"Error occurred: Please import a file first or set the filters correctly.")
				return
			except Exception as e:
				msg = qtw.QErrorMessage()
				msg.showMessage(f"An error occured applying the filter due to: \n{e}.")
				msg.exec_()

	def closeEvent(self, event):
		global live
		global shutdown
		shutdown = True
		if live and len(self.live_data) > 0:
			dt_now = datetime.now()
			dt_now = dt_now.strftime("%d%m%Y_%H%M%S") + ".csv"
			self.dataframe = pd.DataFrame(self.live_data, columns=self.columns)
			print(self.dataframe)
			self.dataframe.to_csv(dt_now, sep=",", index=False)
			try:
				self.worker.stop()
			except:
				pass
		self.logWidget.insertLog("Exiting ESP32 CSI Visualiser")
		import sys
		sys.exit(0)


if __name__ == '__main__':
	import sys
	if len(sys.argv) == 2:
		live = True

	app = qtw.QApplication([])
	app.setStyle('Fusion')
	qt_app = MainWindow()
	qt_app.show()
	app.exec_()
