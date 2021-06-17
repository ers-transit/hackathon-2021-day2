# ERS Pre-launch Data Hackathon | Day 2
This repository contains a tutorial on how to use the eureka package to reduce NIRCam data.

## Getting started
To run the tutorial, you will need simulated NIRCam data and some ancillary files. 
1. Use the terminal to make a directory on your computer to store the simulated data and ancillary files. At the command prompt, enter the following lines (replacing `User` with your home directory name, e.g. `Users/kreidberg`):
    ```
    >> mkdir /User/Data/JWST-Sim/NIRCam/
    >> cd /User/Data/JWST-Sim/NIRCam/
    >> mkdir Stage2
    >> mkdir ancil 
    ```
2. Download the simulated NIRCam data from the [STScI Box site](https://stsci.app.box.com/s/8r6kqh9m53jkwkff0scmed6zx42g307e/folder/135937142862) and save the files in the `Stage2` directory. The files are large (5 GB total) so the download may take a while. If your internet connection is slow, download the [smallest file only](https://stsci.app.box.com/s/8r6kqh9m53jkwkff0scmed6zx42g307e/file/809097167084) and the tutorial will still work.
3. Save the [NIRCam calibration data](https://github.com/ers-transit/hackathon-2021-day2/tree/main/ancil_files/NIRCam) in the `ancil` directory

## Configuring your python environment:
If you have not already installed Anaconda and set up the `ers-transit` environment, please follow the instructions in the Day 0 tutorial: https://github.com/ers-transit/hackathon-2021-day0/blob/main/hackathon-day0-tutorial.ipynb

## Running the tutorial
1. Clone this repository, in one of two ways:
    - if you have git installed, open a terminal window, navigate to the location you want to run the tutorial, and type ``>> git clone https://github.com/ers-transit/hackathon-2021-day2.git``
    - if you do not have git, click on the green ``Code`` button in the upper right of this page and then click ``Download ZIP``
2. Activate the ers-transit conda environment using ``conda activate ers-transit``
3. Open the file S3_wasp43b.ecf and update the three directories at the end of the file (topdir, datadir, and ancildir) to the directories you created in Step 1 of ``Getting Started``.
4. Open a jupyter notebook by typing ``jupyter notebook`` in your terminal window.
5. On the screen that opens, click ``hackathon-day2-tutorial.ipynb`` to start.
