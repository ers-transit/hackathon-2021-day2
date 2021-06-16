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
3. Download the simulated NIRCam data from the [STScI Box site](https://stsci.app.box.com/s/8r6kqh9m53jkwkff0scmed6zx42g307e/folder/135937142862) and save the files in the `Stage2` directory. The files are large (5 GB total) so the download may take a while. If your internet connection is slow, download the [smallest file only](https://stsci.app.box.com/s/8r6kqh9m53jkwkff0scmed6zx42g307e/file/809097167084) and the tutorial will still work.
4. Save the [NIRCam ancillary data](https://github.com/ers-transit/hackathon-2021-day2/tree/main/ancil_files/NIRCam) in the `ancil` directory

## Configuring your python environment:
If you have not already installed Anaconda and set up the `ers-transit` environment, please follow the instructions in the Day 0 tutorial: https://github.com/ers-transit/hackathon-2021-day0/blob/main/hackathon-day0-tutorial.ipynb

