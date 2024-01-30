from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from importFileWidget import importFile
from filterWidget import filterWidget
from mplWidget import Mpl
from worker import Worker
from utils import process, CSVparser

import pandas as pd
import re
from datetime import datetime

live = False

class MainWindow(qtw.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("ESP32 CSI Visualiser")
		self.setWindowIcon(qtg.QIcon('audio-waves.png'))
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

		self.importFileWidget = importFile()
		self.importFileWidget.file.textChanged.connect(
			lambda: self.CSVparserwrapper(self.importFileWidget.getCSVFileName()))
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

			# set the object name as the index, it will be a one to one mapping with the plot
			newfilterWidget.setObjectName(str(len(self.filterWidgets)))

			if not live:
				# need to use lambdas to send arguments
				plotLambda = lambda: self.plotter(newfilterWidget)
				newfilterWidget.mac_address.currentTextChanged.connect(plotLambda)
				newfilterWidget.subcarrier.currentTextChanged.connect(plotLambda)

			self.rightgrid.addWidget(newfilterWidget)
			self.filterWidgets.append(newfilterWidget)

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

			self.mplCanvas.pop()
			self.filterWidgets.pop()

	def live_plotting(self):
		for idx in range(len(self.filterWidgets)):
			filterWidgetObject = self.filterWidgets[idx]
			MAC, subcarrier, index = filterWidgetObject.getAttributes()
		
			try:
				# list of list of CSI data
				csi = self.CSI_DATA[MAC]
				#get the last 100 lists
				csi = csi[-100:]
				
				Y = [x[subcarrier] for x in csi if len(x) > subcarrier]
				X = [i+1 for i in range(len(Y))]
				
				self.mplCanvas[idx].plot(X, Y, f"Amplitude plot of subcarrier {subcarrier}")
			except:
				return
		

	def reportProgress(self, result):
		result = result.split(",")
		
		if len(self.columns) == 0:
			self.columns = result
			return
		
		try:
			result[18] = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
			self.live_data.append(result)
			amp = process(result[25])
			print(amp)
			MAC = result[2]
				
			if len(amp) > 0:
				if MAC in self.CSI_DATA:
					self.CSI_DATA[MAC].append(amp)
				else:
					self.CSI_DATA[MAC] = []
					self.CSI_DATA[MAC].append(amp)
					for filterWidget in self.filterWidgets:
						filterWidget.addToComboBox([MAC])
						
					if self.macAddresses == None:
						self.macAddresses = [MAC]
					
					if self.macAddresses and MAC not in self.macAddresses:
						self.macAddresses.append(MAC)
						
		except:
			return
				

	def CSVparserwrapper(self, CSVFile):
		self.CSI_DATA, self.macAddresses = CSVparser(CSVFile)

		for i in self.filterWidgets:
			i.addToComboBox(self.macAddresses)

	def plotter(self, filterWidgetObject):
		if live == False:
			MAC, subcarrier, index = filterWidgetObject.getAttributes()

			amplitudes = self.CSI_DATA[MAC]
			Y = [x[subcarrier] for x in amplitudes if len(x) > subcarrier]
			X = [i + 1 for i in range(len(Y))]
			self.mplCanvas[int(index)].plot(X, Y, f"Amplitude plot of subcarrier {subcarrier}")

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
