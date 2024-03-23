Final Year Project (SCSE23-0363)

# About
The codes shown in this repository was written for the final year project (SCSE23-0363) in NTU.

The goals of the final year project was:
1. To build a GUI that can parse, process and visualise CSI data captured using the ESP32 CSI Tool.
2. Investigate the feasibility of performing respiration sensing using the ESP32 CSI Tool.
3. To build a keystroke inference system using the ESP32 CSI Tool for CSI collection and a deep learning model for keystroke inference.

This `README.md` shows the file found in this folder, and instructions to setup and run the codes.

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
Final Report
├── README.MD                               # Instructions for running the codes
├── README.txt                              # Instructions for running the codes
├── requirements.txt                        # Contains the packages and libraries needed to run all the code
├── SCSE23_0363_Final_Report.pdf            # Final Report for SCSE23_0363
├── implementation                          # Codes and scripts written for the FYP
│   ├── Scripts                             # Scripts used for keystroke inference and respiration sensing
│   │   ├── data_collection.py              # Script used to collect keystroke inference data
│   │   ├── data_generation.py              # Script used to generate keystroke inference data
│   │   ├── plot_principal_comp.py          # Script used to plot the 4th principal component
│   │   └── processCSV.py                   # Script used to process raw keystroke inference data
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
To run the ESP32 CSI Visualiser, open up command prompt and run the following command. This activates the virtual environment.

```cmd
.venv\Scripts\activate
python main.py
```

To run the codes for the model, open up command prompt and run the following command.
```cmd
.venv\Scripts\activate
jupyter labs
```

This opens up the Jupyter Lab environment which opens in a browser tab. In the left panel, double-click on the "Source Code" folder to enter it. Double-click on any notebook to open it in the right panel. You should be able to see the code now on the right panel.
At the top left, click on "Run", then "Run All Cells" which will run all the code in that notebook. 

# Acknowledgements