Final Year Project (SCSE23-0363)

# About
The codes shown in this repository was written for the final year project (SCSE23-0363) in NTU.

The objectives of the final year project was:
1. To build a GUI that can parse, process and visualise CSI data captured using the ESP32 CSI Tool and the ESP32 microcontroller.
2. To Investigate the feasibility of performing respiration sensing using the ESP32 CSI Tool and the ESP32 microcontroller.
3. To build a keystroke inference system using the ESP32 CSI Tool and the ESP32 microcontroller for CSI collection and a deep learning model for keystroke inference.

This `README.md` shows the files found in this folder, and instructions to setup and run the codes.

# Setting up

The following instructions setups a new virtual environment for python and installs the needed libraries.
These instructions assumes that the user is using a Windows machine. Ensure that Python 3.10 is installed as well. Open the command prompt in the root directory and enter the following commands inside the root directory `FYP`.

```cmd
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Alternatively, you can run the following instructions to setup a new virtual environment for python and installs the needed libraries. This uses the default python version installed in the machine. Open the command prompt in the root directory and enter the following commands inside the root directory `FYP`.
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
├── documentation                           # Stores images used for documentation purposes
│   └── images                              # Images used in README.md
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
To run the ESP32 CSI Visualiser run the following commands.

```cmd
cd implementation\ESP32_CSI_Visualiser
python main.py
```

To re-process and generate a new set of processed data from the raw keystroke inference data run the following commands.

```cmd
cd implementation\Scripts
python processCSV.py
```

To run the codes for the model and run the following command.
```cmd
jupyter lab
```

This opens up the Jupyter Lab environment which opens in a browser tab. In the left panel, double-click on the `implementation` folder to enter it, then double-click again on the `neuralNetwork` folder to enter it. Double-click on `model.ipynb` to open it in the right panel. You should be able to see the code now on the right panel.
At the top left, click on "Run", then "Run All Cells" which will run all the code in that notebook. 

To only plot the fourth principal component using a script. Replace the file_location with the location of the respiration data (`..\..\data\respiration\data`), MAC with the MAC address of the receiver ("B0:CA:68:91:B2:F5") and png_file_name as the output file name.

```cmd
cd implementation\Scripts
python plot_principal_comp.py <file_location> <MAC> <png_file_name>
```

# ESP32 CSI Visualiser

The ESP32 CSI Visualiser supports parsing, plotting and processing of raw CSI data from the ESP32 CSI Tool. The following image shows the UI elements of the tool.

![UI](documentation/images/UI.png)

## Import and Parse files

To import CSV files containing raw CSI data, use the "Browse" button to search and import the CSV file. 

![Import](documentation/images/Import.png)

## Process and Filter files

After importing the file, use the following widget to process and filter the CSI data. 

![Process](documentation/images/Process.png)

There are 3 types of filters supported: (1) 2nd-order Butterworth low-pass filter, (2) Hampel filter, and (3) Discrete Wavelet Transform (DWT).

For the Butterworth low-pass filter, one needs to set both the cutoff frequency, and sampling frequency.
For Hampel filter and DWT, one needs to set the Window/ Wavelet(db) used.

Three types of graphs are supported. The first is a normal plot, and one needs to choose the subcarrier to plot. The second is a heatmap that plots all subcarriers. The last plot supported is the principal component analysis (PCA).
Filters are automatically applied to the amplitude or phase, before being plotted.

The tool supports plotting against time and packets by checking the button "X-axis: Time". Also, one can choose to plot either the CSI amplitude or phase by using the CSI dropdown.

After setting up all the parameters, click on the "Apply filter" button to plot the CSI data.

## Plotting

The tool supports multiple plots up to 4 different plots. To add more canvas for plotting, click on the "Add Graph" button and to remove canvas, click on the "Remove Graph" button. The following image shows the CSI amplitude of subcarrier 17. The top graph (Graph 1) is the plot before, while the bottom graph (Graph 2) had a Butterworth low-pass filter applied.

![Processed_plot](documentation/images/Processed_Plot.png)

Therefore, the multiple plots allows users to compare either between different subcarriers, or to look at the results of applying filters on the CSI data.
