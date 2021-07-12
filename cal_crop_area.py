# Standard Library Imports
import os
import argparse
import multiprocessing
import fnmatch
#import geopandas as gpd
import rasterio as rio
import glob
import numpy as np
import matplotlib.pyplot as plt
import fiona
from fiona.crs import from_epsg
from rasterio.plot import plotting_extent,show
from rasterio.mask import mask
import gdal
import shutil

shape_path = "/home/gift/Downloads/Shapefiles/Study_lakes/Boundary/Boundary.shp"

def main(runDir):
    # list all subdirectories:
    allSubContents = os.listdir(runDir)

    # These are the directories to find landsat files
    allSubDirs = [f"{runDir}/{i}" for i in allSubContents if os.path.isdir(f"{runDir}/{i}")]

    for dirs in allSubDirs:
        lan10 = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*B10.TIF')]
        lan5 = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*B5.TIF')]
        lan4 = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*B4.TIF')]
        mtl = [file for file in os.listdir(dirs) if fnmatch.fnmatch(file, '*MTL.txt')]
        land10 = lan10[0]
        land5 = lan5[0]
        land4 = lan4[0]
        mtl1 = mtl[0]
        la_10 = os.path.join(dirs,land10)
        la_5 = os.path.join(dirs,land5)
        la_4 = os.path.join(dirs,land4)
        mtl_file = os.path.join(dirs,mtl1)

        folder = os.path.join(os.path.dirname(runDir), os.path.basename(runDir)+ "_output")
        if not os.path.exists(folder):
            os.mkdir(folder)
        storage = os.path.join(folder,"cropfiles")
        if not os.path.exists(storage):
            os.mkdir(storage)
        dump = os.path.join(folder,"dump")
        if not os.path.exists(dump):
            os.mkdir(dump)
        mtls = os.path.join(folder,"mtls")
        if not os.path.exists(mtls):
            os.mkdir(mtls)
        sub_storage = os.path.join(storage,land4[:-7])
        if not os.path.exists(sub_storage):
            os.mkdir(sub_storage)

        shutil.copy(mtl_file, mtls)

        input_1 = gdal.Open(la_10)
        la10 = (os.path.join(dump, land10[:-4])+"_"+".tif")
        input_2 = gdal.Open(la_5)
        la5 = (os.path.join(dump, land5[:-4])+"_"+".tif")
        input_3 = gdal.Open(la_4)
        la4 = (os.path.join(dump, land4[:-4])+"_"+".tif")

        gdal.Warp(la10 , input_1, dstSRS='EPSG:26911')
        gdal.Warp(la5 , input_2, dstSRS='EPSG:26911')
        gdal.Warp(la4 , input_3, dstSRS='EPSG:26911')


        #set spatial reference and transformation:
        with fiona.open(shape_path, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]

        with rio.open(la10) as land_B10:
            out_image, out_transform = rio.mask.mask(land_B10, shapes, crop=True)
            out_meta = land_B10.meta

        out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})

        with rio.open(os.path.join(sub_storage,land10[:-4]) + ".tif", 'w', **out_meta) as dst:
            dst.write(out_image)

        with rio.open(la5) as land_B5:
            out_image, out_transform = rio.mask.mask(land_B5, shapes, crop=True)
            out_meta = land_B5.meta

        out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})

        with rio.open(os.path.join(sub_storage,land5[:-4]) + ".tif", 'w', **out_meta) as dst:
            dst.write(out_image)

        with rio.open(la4) as land_B4:
            out_image, out_transform = rio.mask.mask(land_B4, shapes, crop=True)
            out_meta = land_B4.meta

        out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})

        with rio.open(os.path.join(sub_storage,land4[:-4]) + ".tif", 'w', **out_meta) as dst:
            dst.write(out_image)
    
    shutil.rmtree(dump)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
        For creating temperature from Landsat 8
    """)
    parser.add_argument('rundir',
                        type=str,
                        help="The path to the run directory with the landsat files")
    args = parser.parse_args()
    main(os.path.abspath(args.rundir))

