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
        lan10 = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*B10.tif')]
        lan5 = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*B5.tif')]
        lan4 = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*B4.tif')]
        land10 = lan10[0]
        land5 = lan5[0]
        land4 = lan4[0]
        la10 = os.path.join(dirs,land10) 
       # print(la10)
        la5 = os.path.join(dirs,land5) 
       # print(la5)
        la4 = os.path.join(dirs,land4)
        #print(la4) 

        with rio.open(la10) as land_B10:
            l10 = land_B10.read(1)

        with rio.open(la5) as land_B5:     
            l5 = land_B5.read(1)
        

        with rio.open(la4) as land_B4:
            l4 = land_B4.read(1)
    
        np.seterr(divide='ignore', invalid='ignore')

        rad10 = 0.0003342 * l10 + 0.1

        tb10 = (1321.0789/np.log((774.8853/rad10)+1)) - 273.15

        ndvi_lower = (l5.astype(float) + l4.astype(float))
        ndvi_upper = (l5.astype(float) - l4.astype(float))
        ndvi = ndvi_upper/ndvi_lower

        #max = np.nanmax(ndvi)
        #min = np.nanmin(ndvi)

        pv = np.square((ndvi  + 1)/(1+1))

        e = 0.004 * pv + 0.986

        t = tb10/(1+(10.8*tb10/14388)* np.log(e))

        kwargs = land_B10.meta
        kwargs.update(
            dtype=rio.float32,
            count=1,
            compress='lzw')
        
        storage = os.path.join(os.path.dirname(runDir),'Landsat_LST')
        if not os.path.exists(storage):
            os.mkdir(storage)
        sub_storage = os.path.join(storage,land4[:-7])
        if not os.path.exists(sub_storage):
            os.mkdir(sub_storage)
        with rio.open(os.path.join(sub_storage,land4[:-7]) + ".tif", 'w', **kwargs) as dst:
            dst.write_band(1, t.astype(rio.float32))

        #plt.imshow(t)
        
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