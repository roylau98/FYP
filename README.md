FYP Implementation Project

# About
The codes shown in this repository was written for the final year project (SCSE23-0363) in NTU.

The goals of the final year project was:
1. To build a GUI that can parse, process and visualise CSI data captured using the ESP32 CSI Tool.
2. Investigate the feasibility of performing respiration sensing using the ESP32 CSI Tool.
3. To build a keystroke inference system using the ESP32 CSI Tool for CSI collection and a deep learning model for keystroke inference.
# Setting up

The following instructions setups a new virtual environment for python and installs the needed libraries.
These instructions assumes that the user is using a Windows machine. Ensure that Python 3.10 is installed as well, do not use Python 3.12. Open the command prompt in the root directory "" and enter the following commands.

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

# Directory structure

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