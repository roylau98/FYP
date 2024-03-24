Final Year Project (SCSE23-0363)

# About
The codes shown in this repository was written for the final year project (SCSE23-0363) in NTU.

The goals of the final year project was:
1. To build a GUI that can parse, process and visualise CSI data captured using the ESP32 CSI Tool.
2. Investigate the feasibility of performing respiration sensing using the ESP32 CSI Tool.
3. To build a keystroke inference system using the ESP32 CSI Tool for CSI collection and a deep learning model for keystroke inference.

This `README.md` shows the files found in this folder, and instructions to setup and run the codes.

# Setting up

The following instructions setups a new virtual environment for python and installs the needed libraries.
These instructions assumes that the user is using a Windows machine. Ensure that Python 3.10 is installed as well, do not use Python 3.12. Open the command prompt in the root directory and enter the following commands.

```cmd
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Alternatively, you can run the following instructions to setup a new virtual environment for python and installs the needed libraries. This uses the default python version installed in the machine.
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

# Folder struture and files

The following is a tree structure that shows the files found in this folder. A brief description of what each file is for is included at the side.

```markdown
FYP
├── README.MD                               # Instructions for running the codes
├── README.txt                              # Instructions for running the codes
├── requirements.txt                        # Contains the packages and libraries needed to run all the code
├── implementation                          # Codes and scripts written for the FYP
│   ├── Scripts                             # Scripts used for keystroke inference and respiration sensing
│   │   ├── data_collection.py              # Script used to collect keystroke inference data
│   │   ├── data_generation.py              # Script used to generate keystroke inference data
│   │   ├── plot_principal_comp.py          # Script used to plot the 4th principal component
│   │   ├── processCSV.py                   # Script used to process raw keystroke inference data
│   │   └── utils.py                        # Utility functions
│   ├── neuralNetwork                       # Jupyter Notebook for the model
│   │   ├── model.ipynb                     # Model used for keystroke inference
│   └── ESP32_CSI_Visualiser                # Code for implementing the ESP32 CSI Visualiser
│       ├── main.py                         # Main.py for ESP32 CSI Visualiser
│       ├── utilities                       # Utility functions
│       ├── userInterface                   # User Interface elements
│       └── resources                       # Image resources used
└── data                                    # Contains all CSI data for respiration sensing and keystroke inference
    ├── sample_data.csv                     # Sample CSI data 
    ├── respiration_data                    # Raw data for respiration sensing
    ├── processed_data                      # Processed data for keystroke inference
    └── keystroke_inference_raw             # Unprocessed raw data for keystroke inference
```

Codes for the model is given in the form of a Jupyter notebook. To re-process the raw keystroke inference file, one should remove the files found in `data\processed_data` before running the python file `Scripts\processCSV.py`

The codes for the ESP32 CSI Visualiser is found in `ESP32_CSI_Visualiser`. Sample data, and respiration data collected can be found in the `data\sample_data.csv` and the `data\respiration_data` folder.

# Running the code
Before running any code or commands, ensures that the virtual environment is activated. Do this by running the following commands in the root directory `FYP`
```cmd
.venv\Scripts\activate
```
To run the ESP32 CSI Visualiser, open up command prompt in the root directory `FYP` and run the following commands.

```cmd
cd implementation\ESP32_CSI_Visualiser
python main.py
```

To re-process and generate a new set of processed data from the raw keystroke inference data, open up command prompt in the root directory `FYP` and run the following commands.

```cmd
cd implementation\Scripts
python processCSV.py
```

To run the codes for the model, open up command prompt in the root directory `FYP` and run the following command.
```cmd
jupyter lab
```

This opens up the Jupyter Lab environment which opens in a browser tab. In the left panel, double-click on the `implementation` folder to enter it, then double-click again on the `neuralNetwork` folder to enter it. Double-click on `model.ipynb` to open it in the right panel. You should be able to see the code now on the right panel.
At the top left, click on "Run", then "Run All Cells" which will run all the code in that notebook. 

# ESP32 CSI Visualiser

The ESP32 CSI Visualiser supports parsing, plotting and processing of raw CSI data from the ESP32 CSI Tool. The following image shows the UI elements of the tool.

![UI](documentation\images\UI.png)

## Import and Parse files

To import CSV files containing raw CSI data, use the "Browse" button to search and import the file. 

![UI](documentation\images\Import.png)

## Process and Filter files

After importing the file, use the following widget to process and filter the CSI data. 

![UI](documentation\images\Process.png)

There are 3 types of filters supported: (1) 2nd-order Butterworth low-pass filter, (2) Hampel filter, and (3) Discrete Wavelet Transform (DWT).

For the Butterworth low-pass filter, one needs to set both the cutoff frequency, and sampling frequency.
For Hampel filter and DWT, one needs to set the Window/ Wavelet(db) used.

Three types of graphs are supported. The first is a normal plot, and one needs to choose the subcarrier to plot. The second is a heatmap that plots all subcarriers. The last plot supported is the principal component analysis (PCA).
Filters are automatically applied to the raw data, before being plotted.