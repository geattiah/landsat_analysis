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
#import shapefile as shpp

tiff = "/home/gift/Documents/Landsat/new_landsat_output/cropfiles/LC08_L1GT_046016_20190210_20190222_01_T2/LC08_L1GT_046016_20190210_20190222_01_T2_B5.tif"
shape = "/home/gift/Downloads/Shapefiles/Study_lakes/Sel_lakes/Frame_Lake.shp"

with rio.open(tiff) as lake_temp:
    p = lake_temp.read(1)
with fiona.open(shape, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]   

# cmap="gist_rainbow_r"
# plt.imshow(p, cmap=cmap,interpolation="hermite")
# plt.clim(23,15)
# plt.colorbar().set_label('Temperature (°C)')
# plt.title("Frame_Lake")
# fig_loc = "/home/gift/Documents/research/images/LST"
#fig_file = os.path.join(fig_loc,(str(files)[17:25])+(str(files)[40:-4]))
#plt.savefig(fig_file)   # save the figure to file
plt.imshow(p)
plt.show()