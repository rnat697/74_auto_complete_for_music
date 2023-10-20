# AutoComplete for Music - PyQt demo
-  Make sure you have python 38 and pip installed:
    - Download and install miniconda from https://docs.conda.io/en/latest/miniconda.html and select the python 3.8 windows version.
    - Open up the Anaconda prompt and copy this command conda create –n py38 python=3.8 and paste it in the prompt. Press and enter y when prompted. 
    - Once environment has been created write this command conda activate py38 on the prompt to activate the py38 environment. Your environment will change from (base) to (py38)
- Install all the packages in requirements.txt using `pip install -r requirements.txt`
- Create an environment variable for FluidSynth on your Windows system. (Add the `fluidsynth-x64\bin` subdirectory to your PATH. To do this, click in the search box on the taskbar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. `c:\Users\me\install\fluidsynth-x64\bin.`) https://ksvi.mff.cuni.cz/~dingle/2019/prog_1/python_music.html


## Interactive Demonstration 
The interactive demonstration is under the `pyqt_demo_code` folder. In that folder, please read the README.md for project setup. Once you have installed the required packages and set up FluidSynth, here is some instructions on how to run:
1. Change your directory to the `pyqt_demo_code` folder using `cd pyqt_demo_code`
2. Run the `music_gen_demo.py` file using the run button or type `python music_gen_demo.py` in command line.

Note: that the files generated (i.e. wav and midi files) are located in `pyqt_demo_code/music_python/outputs` folder.