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

shapefolder = "/home/gift/Downloads/Shapefiles/Study_lakes/Sel_lakes"


def main(runDir):
    # list all subdirectories:
    allSubContents = os.listdir(runDir)
   
    # These are the directories to find landsat files
    allSubDirs = [f"{runDir}/{i}" for i in allSubContents if os.path.isdir(f"{runDir}/{i}")]

    for dirs in allSubDirs:
        for files in os.listdir(dirs):
            if files.endswith('.tif'):
                filepath = os.path.join(dirs, files)
                storage = os.path.join(os.path.dirname(runDir),'LST_All_lakes')
                if not os.path.exists(storage):
                    os.mkdir(storage)
                sub_storage = os.path.join(storage,files[:-4])
                if not os.path.exists(sub_storage):
                    os.mkdir(sub_storage)
                    for cfiles in os.listdir(shapefolder):
                        if cfiles.endswith('.shp'):
                            shapepath = os.path.join(shapefolder, cfiles)
                            with fiona.open(shapepath, "r") as shapefile:
                                shapes = [feature["geometry"] for feature in shapefile]
            
                            with rio.open(filepath) as src:
                                out_image, out_transform = rio.mask.mask(src, shapes, crop=True, nodata=float('NaN'))
                                out_meta = src.meta

                            out_meta.update({"driver": "GTiff",
                                            "height": out_image.shape[1],
                                            "width": out_image.shape[2],
                                            "transform": out_transform})

                            with rio.open(os.path.join(sub_storage,files[:-4])+ "_" + cfiles[:-4] + ".tif", "w", **out_meta) as dest:
                                dest.write(out_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        For creating temperature from Landsat 8
    """)
    parser.add_argument('rundir',
                        type=str,
                        help="The path to the run directory with the landsat files")
    args = parser.parse_args()
    main(os.path.abspath(args.rundir))                                     