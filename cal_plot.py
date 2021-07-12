# Standard Library Imports
import os
import argparse
import multiprocessing
import fnmatch
import rasterio as rio
import glob
import numpy as np
import matplotlib.pyplot as plt
import fiona
from rasterio.plot import plotting_extent,show
from rasterio.mask import mask

shapefolder = "C:\\Users\\attiah\\Downloads\\Sel_lakes (1)\\Sel_lakes"

def main(runDir):
    # list all subdirectories:
    allSubContents = os.listdir(runDir)
   
    # These are the directories to find landsat files
    allSubDirs = [f"{runDir}/{i}" for i in allSubContents if os.path.isdir(f"{runDir}/{i}")]

    for dirs in allSubDirs:
        for files in os.listdir(dirs):
            fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
            file_out = os.path.join(dirs, files)
            with rio.open(file_out) as lake_temp:
                p = lake_temp.read(1)
            cmap= "gist_rainbow_r"
            plt.imshow(p, cmap=cmap)
            plt.clim(-20,25)
            plt.colorbar().set_label('Temperature (°C)')
            plt.title((str(files)[17:25])+(str(files)[40:-4]))
            fig_loc = "/home/gift/Documents/Landsat/2001_data/extracted/2001__output/lst_images"

            fig_file = os.path.join(fig_loc,(str(files)[17:25])+(str(files)[40:-4]))
            plt.savefig(fig_file) 
    #plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        For creating temperature from Landsat 8
    """)
    parser.add_argument('rundir',
                        type=str,
                        help="The path to the run directory with the landsat files")
    args = parser.parse_args()
    main(os.path.abspath(args.rundir))                                     