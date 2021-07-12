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
    #mtldirectory = os.path.join(os.path.dirname(runDir),'mtls')

    # = os.listdir(os.path.join(os.path.dirname(runDir),'mtls'))
    #print(allSubContents)
   
    # These are the directories to find landsat files
    allSubDirs = [f"{runDir}/{i}" for i in allSubContents if os.path.isdir(f"{runDir}/{i}")]
    #print(allSubDirs)
    for dirs in allSubDirs:
        for files in os.listdir(dirs):
            tif = os.path.join(dirs,files)
            print(tif)
            #mtl = [mtls for mtls in mtldirectories if fnmatch.fnmatch(mtls, str(files[:-4]))]
            #print(mtl)
            with rio.open(tif) as lst:
                land_st = lst.read(1)
            
            np.seterr(divide='ignore', invalid='ignore')

            at = land_st - 2.2

            kwargs = lst.meta
            kwargs.update(
                dtype=rio.float32,
                count=1,
                compress='lzw')
            
            storage = os.path.join(os.path.dirname(runDir),'Landsat_AT')
            if not os.path.exists(storage):
                os.mkdir(storage)
            sub_storage = os.path.join(storage,files[:-7])
            if not os.path.exists(sub_storage):
                os.mkdir(sub_storage)
            with rio.open(os.path.join(sub_storage,files[:-4]) + ".tif", 'w', **kwargs) as dst:
                dst.write_band(1, at.astype(rio.float32))

        #plt.imshow(at)

        
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