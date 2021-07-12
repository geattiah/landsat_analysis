# Standard Library Imports
import os
import argparse
import multiprocessing
import fnmatch
import rasterio as rio
import glob
import numpy as np
import matplotlib.pyplot as plt


def main(runDir):
    # list all subdirectories:
    allSubContents = os.listdir(runDir)
   
    # These are the directories to find landsat files
    allSubDirs = [f"{runDir}/{i}" for i in allSubContents if os.path.isdir(f"{runDir}/{i}")]
    for dirs in allSubDirs:
        for file in os.listdir(dirs):
                la10 = [os.path.join(dirs,file) if fnmatch.fnmatch(file, '*B10.TIF')]
                print(la10)
                
            elif fnmatch.fnmatch(file, '*B5.TIF'):
                la5 = os.path.join(dirs,file)
                return la5

            elif fnmatch.fnmatch(file, '*B1.TIF'):
                la4 = os.path.join(dirs,file)
                return la4

                # with rio.open(la10) as land_B10:
                #     l10 = land_B10.read(1)

                # with rio.open(la5) as land_B5:     
                #     l5 = land_B5.read(1)
                
                # with rio.open(la4) as land_B4:
                #     l4 = land_B4.read(1)
            
                # np.seterr(divide='ignore', invalid='ignore')

                # rad10 = 0.0003342 * l10 + 0.1

                # tb10 = (1321.0789/np.log((774.8853/rad10)+1)) - 273.15

                # ndvi_lower = (l5.astype(float) + l4.astype(float))
                # ndvi_upper = (l5.astype(float) - l4.astype(float))

                # ndvi = ndvi_upper/ndvi_lower

                # #max = np.nanmax(ndvi)

                # #min = np.nanmin(ndvi)

                # pv = np.square((ndvi  + 1)/(1+1))
                # print(pv)
                # e = 0.004 * pv + 0.986

                # t = tb10/(1+(10.8*tb10/14388)* np.log(e))

                # plt.imshow(t)
                
                # plt.show()

                # print("true")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        For creating plots from the output of CLIMoGrid
    """)
    parser.add_argument('rundir',
                        type=str,
                        help="The path to the run directory with run_info.txt file")
    args = parser.parse_args()
    main(os.path.abspath(args.rundir))                                     